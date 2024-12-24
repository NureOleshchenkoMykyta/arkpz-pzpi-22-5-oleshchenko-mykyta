from flask import Flask, jsonify, request, redirect
from flasgger import Swagger
from database import execute_query


app = Flask(__name__)
app.config['SWAGGER'] = {
    'title': 'API Documentation',
    'uiversion': 3,
    'version': '1.0.0',
    'description': 'Документація для API'
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # Усі маршрути включено
            "model_filter": lambda tag: True,  # Усі моделі включено
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}

swagger = Swagger(app, config=swagger_config)

@app.route('/')
def index():
    return redirect('/docs')

@app.route('/docs')
def docs():
    return redirect('/apidocs')

@app.route('/register', methods=['POST'])
def register():
    """
    register
    ---
    tags:
      - Account
    operationId: "Реєстрація нового акаунта"
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Електронна пошта користувача
              example: "example@gmail.com"
            password:
              type: string
              description: Пароль користувача
              example: "password123"
            name:
              type: string
              description: Ім'я користувача
              example: "John Doe"
    responses:
      200:
        description: Акаунт успішно створено
      400:
        description: Невірний запит
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if not email or not password or not name:
        return jsonify({"error": "Поля email, password, and name повинні бути заповнені"}), 400

    query = """
    INSERT INTO analysisstate.account (Email, Password, Name)
    VALUES (%s, %s, %s);
    """
    params = (email, password, name)

    execute_query(query, params)
    result = execute_query(query, params)
    if result is None:
        print("Запит виконаний успішно, але дані не повернуто.")
    else:
        print("Результат запиту:", result)
    return jsonify({"message": "Акаунт успішно створено"}), 200



# Логін користувача
@app.route('/login', methods=['POST'])
def login():
    """
    login
    ---
    tags:
      - Account
    operationId: "Логін користувача"
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Електронна пошта користувача
              example: "example@gmail.com"
            password:
              type: string
              description: Пароль користувача
              example: "password123"
    responses:
      200:
        description: Логін успішний
      400:
        description: Неправильний email або пароль
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    query = "SELECT * FROM analysisstate.account WHERE Email = %s AND Password = %s;"
    account = execute_query(query, (email, password))

    if account:
        return jsonify({"message": "Логін успішний"}), 200
    else:
        return jsonify({"message": "Неправильний email або пароль"}), 400

# Отримати всі аккаунти
@app.route('/accounts', methods=['GET'])
def get_all_accounts():
    """
    get_all_accounts
    ---
    tags:
      - Account
    operationId: "Отримати всі акаунти"
    responses:
      200:
        description: Список акаунтів
        schema:
          type: array
          items:
            type: object
            properties:
              AccountID:
                type: integer
              Email:
                type: string
              Name:
                type: string
    """
    query = "SELECT AccountID, Email, Name FROM analysisstate.account;"
    accounts = execute_query(query)

    return jsonify(accounts), 200


# Видалення акаунта по e-mail
@app.route('/accounts', methods=['DELETE'])
def delete_account():
    """
    delete_account
    ---
    tags:
      - Account
    operationId: "Видалення акаунта по e-mail"
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: E-mail акаунта для видалення
    responses:
      200:
        description: Акаунт успішно видалено
      400:
        description: Помилка при видаленні акаунта
    """
    email = request.args.get('email')  # Отримуємо e-mail з параметрів запиту

    if not email:
        return jsonify({"message": "Не вказаний e-mail"}), 400

    try:
        # Отримуємо AccountID по e-mail
        account_id_result = execute_query(
            "SELECT AccountID FROM analysisstate.account WHERE Email = %s;", (email,)
        )

        if not account_id_result:
            return jsonify({"message": "Акаунт не знайдено за вказаним e-mail"}), 400

        # Беремо AccountID із результату запиту
        account_id = account_id_result[0][0]  # Отримуємо перший елемент першого кортежу

        # Видалення пов'язаних даних
        execute_query("DELETE FROM analysisstate.results WHERE AccountID = %s;", (account_id,))
        execute_query("DELETE FROM analysisstate.notes WHERE AccountID = %s;", (account_id,))

        # Видалення акаунта
        execute_query("DELETE FROM analysisstate.account WHERE AccountID = %s;", (account_id,))

        return jsonify({"message": "Акаунт і пов'язані дані успішно видалено"}), 200

    except Exception as e:
        return jsonify({"message": f"Помилка при видаленні акаунта: {str(e)}"}), 400


# Зміна паролю
@app.route('/accounts/<string:email>/change-password', methods=['PUT'])
def change_password(email):
    """
    change_password
    ---
    tags:
      - Account
    operationId: "Зміна пароля акаунта"
    parameters:
      - name: email
        in: path
        required: true
        type: string
        description: Email акаунта
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            old_password:
              type: string
              required: true
              description: Старий пароль
            new_password:
              type: string
              required: true
              description: Новий пароль
    responses:
      200:
        description: Пароль успішно змінено
      400:
        description: Невірний старий пароль
    """
    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    # Перевірка старого паролю
    query = "SELECT * FROM analysisstate.account WHERE Email = %s AND Password = %s;"
    account = execute_query(query, (email, old_password))

    if not account:
        return jsonify({"message": "Неправильний старий пароль"}), 400

    # Оновлення паролю
    query = "UPDATE analysisstate.account SET Password = %s WHERE Email = %s;"
    execute_query(query, (new_password, email))

    return jsonify({"message": "Пароль успішно змінено"}), 200


def determine_emotional_state(stress_level):
    """
    Функція для визначення емоційного стану по рівню стресу.
    """
    if stress_level <= 20:
        return "Спокійний"
    elif 21 <= stress_level <= 40:
        return "Незначний"
    elif 41 <= stress_level <= 60:
        return "Середній"
    elif stress_level >= 61:
        return "Тривожний"
    return "Невідомий"  # На всяк випадок, якщо рівень стресу вийде за межі

@app.route('/results', methods=['POST'])
def create_result():
    """
    create_result
    ---
    tags:
      - Results
    operationId: "Додати результат аналізу"
    parameters:
      - name: email
        in: query
        required: true
        type: string
        description: E-mail акаунта для додавання результату
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            stress_level:
              type: integer
              description: Рівень стресу
              example: 75
    responses:
      200:
        description: Результат успішно додано
    """
    email = request.args.get('email')  # Отримуємо e-mail з параметрів запиту
    if not email:
        return jsonify({"message": "Не вказаний e-mail"}), 400

    data = request.get_json()
    stress_level = data.get('stress_level')

    if not stress_level:
        return jsonify({"message": "Рівень стресу є обов'язковим"}), 400

    # Визначаємо emotional_state залежно від stress_level
    emotional_state = determine_emotional_state(stress_level)

    try:
        # Отримуємо AccountID по e-mail
        account_id_result = execute_query(
            "SELECT AccountID FROM analysisstate.account WHERE Email = %s;", (email,)
        )

        if not account_id_result:
            return jsonify({"message": "Акаунт не знайдено за вказаним e-mail"}), 400

        account_id = account_id_result[0][0]  # Отримуємо AccountID

        # Вставлення нового результату в таблицю results
        query = """
        INSERT INTO analysisstate.results (AccountID, StressLevel, EmotionalState)
        VALUES (%s, %s, %s);
        """
        execute_query(query, (account_id, stress_level, emotional_state))

        return jsonify({"message": "Результат успішно додано"}), 200

    except Exception as e:
        return jsonify({"message": f"Помилка при додаванні результату: {str(e)}"}), 400

#Отримання результатів для акаунта
@app.route('/results', methods=['GET'])
def get_results():
    """
    get_results
    ---
    tags:
      - Results
    operationId: "Отримати результати для акаунта"
    parameters:
      - name: email
        in: query
        required: true
        type: string
        description: E-mail акаунта
    responses:
      200:
        description: Список результатів
        schema:
          type: array
          items:
            type: object
            properties:
              ResultID:
                type: integer
              AnalysisDate:
                type: string
              StressLevel:
                type: integer
              EmotionalState:
                type: string
    """
    email = request.args.get('email')  # Отримуємо e-mail з параметрів запиту

    if not email:
        return jsonify({"message": "Не вказаний e-mail"}), 400

    try:
        # Отримуємо AccountID по e-mail
        account_id_result = execute_query(
            "SELECT AccountID FROM analysisstate.account WHERE Email = %s;", (email,)
        )

        if not account_id_result:
            return jsonify({"message": "Акаунт не знайдено за вказаним e-mail"}), 400

        account_id = account_id_result[0][0]  # Отримуємо AccountID

        # Запит для отримання результатів по AccountID
        query = "SELECT * FROM analysisstate.results WHERE AccountID = %s;"
        results = execute_query(query, (account_id,))

        return jsonify(results), 200

    except Exception as e:
        return jsonify({"message": f"Помилка при отриманні результатів: {str(e)}"}), 400


#Оновити результат аналізу
@app.route('/results', methods=['PUT'])
def update_result():
    """
    update_result
    ---
    tags:
      - Results
    operationId: "Оновити результат аналізу"
    parameters:
      - name: email
        in: query
        required: true
        type: string
        description: E-mail акаунта
      - name: result_id
        in: query
        required: true
        type: integer
        description: ID результату
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            stress_level:
              type: integer
              description: Новий рівень стресу
              example: 85
    responses:
      200:
        description: Результат успішно оновлено
    """
    email = request.args.get('email')  # Отримуємо e-mail з параметрів запиту
    result_id = request.args.get('result_id')  # Отримуємо result_id з параметрів запиту

    if not email or not result_id:
        return jsonify({"message": "Не вказаний e-mail або ID результату"}), 400

    data = request.get_json()
    stress_level = data.get('stress_level')

    if not stress_level:
        return jsonify({"message": "Рівень стресу є обов'язковим"}), 400

    # Визначаємо emotional_state залежно від stress_level
    emotional_state = determine_emotional_state(stress_level)

    try:
        # Отримуємо AccountID по e-mail
        account_id_result = execute_query(
            "SELECT AccountID FROM analysisstate.account WHERE Email = %s;", (email,)
        )

        if not account_id_result:
            return jsonify({"message": "Акаунт не знайдено за вказаним e-mail"}), 400

        account_id = account_id_result[0][0]  # Получаем AccountID

        # Оновлюємо результат по result_id
        query = """
        UPDATE analysisstate.results
        SET StressLevel = %s, EmotionalState = %s
        WHERE ResultID = %s AND AccountID = %s;
        """
        execute_query(query, (stress_level, emotional_state, result_id, account_id))

        return jsonify({"message": "Результат успішно оновлено"}), 200

    except Exception as e:
        return jsonify({"message": f"Помилка при оновленні результату: {str(e)}"}), 400


#Видалити результат аналізу
@app.route('/results', methods=['DELETE'])
def delete_result():
    """
    delete_result
    ---
    tags:
      - Results
    operationId: "Видалити результат аналізу"
    parameters:
      - name: email
        in: query
        required: true
        type: string
        description: E-mail акаунта
      - name: result_id
        in: query
        required: true
        type: integer
        description: ID результату
    responses:
      200:
        description: Результат успішно видалений
    """
    email = request.args.get('email')  # Отримуємо e-mail із параметрів запиту
    result_id = request.args.get('result_id')  # Отримуємо result_id із параметрів запиту

    if not email or not result_id:
        return jsonify({"message": "Не вказаний e-mail або ID результату"}), 400

    try:
        # Отримуємо AccountID по e-mail
        account_id_result = execute_query(
            "SELECT AccountID FROM analysisstate.account WHERE Email = %s;", (email,)
        )

        if not account_id_result:
            return jsonify({"message": "Акаунт не знайдено за вказаним e-mail"}), 400

        account_id = account_id_result[0][0]  # Отримуємо AccountID

        # Видаляємо результат
        query = "DELETE FROM analysisstate.results WHERE ResultID = %s AND AccountID = %s;"
        execute_query(query, (result_id, account_id))

        return jsonify({"message": "Результат успішно видалений"}), 200

    except Exception as e:
        return jsonify({"message": f"Помилка при видаленні результату: {str(e)}"}), 400


#Створити нотатку
@app.route('/notes', methods=['POST'])
def create_note():
    """
    create_note
    ---
    tags:
      - Notes
    operationId: "Створити нотатку"
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            account_id:
              type: integer
              description: ID акаунта
              example: 1
            text:
              type: string
              description: Текст нотатки
              example: "Це моя нотатка"
    responses:
      200:
        description: Нотатка успішно створена
    """
    data = request.get_json()
    account_id = data.get('account_id')
    text = data.get('text')

    query = """
    INSERT INTO analysisstate.notes (AccountID, Text)
    VALUES (%s, %s);
    """
    execute_query(query, (account_id, text))

    return jsonify({"message": "Нотатка успішно створена"}), 200

#Отримати всі нотатки для акаунта
@app.route('/accounts/<int:account_id>/notes', methods=['GET'])
def get_notes(account_id):
    """
    get_notes
    ---
    tags:
      - Notes
    operationId: "Отримати всі нотатки для акаунта"
    parameters:
      - name: account_id
        in: path
        type: integer
        required: true
        description: ID акаунта
    responses:
      200:
        description: Список нотаток
        schema:
          type: array
          items:
            type: object
            properties:
              NoteID:
                type: integer
              CreationDate:
                type: string
              Text:
                type: string
    """
    query = "SELECT * FROM analysisstate.notes WHERE AccountID = %s;"
    notes = execute_query(query, (account_id,))
    return jsonify(notes), 200

#Оновити нотатку
@app.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """
    update_note
    ---
    tags:
      - Notes
    operationId: "Оновити нотатку"
    parameters:
      - name: note_id
        in: path
        required: true
        type: integer
        description: ID нотатки
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              description: Новий текст нотатки
              example: "Оновлений текст нотатки"
    responses:
      200:
        description: Нотатка успішно оновлена
    """
    data = request.get_json()
    text = data.get('text')

    query = "UPDATE analysisstate.notes SET Text = %s WHERE NoteID = %s;"
    execute_query(query, (text, note_id))

    return jsonify({"message": "Нотатка успішно оновлена"}), 200

#Видалити нотатку
@app.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """
    delete_note
    ---
    tags:
      - Notes
    operationId: " "
    parameters:
      - name: note_id
        in: path
        required: true
        type: integer
        description: ID нотатки
    responses:
      200:
        description: Нотатка успішно видалена
    """
    query = "DELETE FROM analysisstate.notes WHERE NoteID = %s;"
    execute_query(query, (note_id,))

    return jsonify({"message": "Нотатка успішно видалена"}), 200


if __name__ == '__main__':
    app.run(debug=True)
