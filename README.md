# **Lettuce Event-Driven System**
A simple event-driven system using **RabbitMQ** as a message broker. It mimics **Blinker-like signals** but allows **cross-service communication** using a publish-subscribe model.

## **🚀 Getting Started**

### **1️⃣ Prerequisites**
Ensure you have the following installed:
- **Python 3.x**
- **Poetry** (Dependency management)
- **Docker & Docker Compose** (For RabbitMQ)
- **pip** (Python package manager)
- **A virtual environment (optional, but recommended)**

### **2️⃣ Installing Poetry**
This project uses **Poetry** for dependency management.
If you haven't installed it yet, run:
```bash
pip install poetry
```
or use the official installer:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
Verify installation:
```bash
poetry --version
```

### **3️⃣ Setting Up RabbitMQ**
This project includes a **Docker Compose** configuration (`broker/rabbitmq.yml`) to quickly spin up a RabbitMQ instance.

#### **🚀 Start RabbitMQ Using Docker Compose**
```bash
docker-compose -f broker/rabbitmq.yml up -d
```
This will:
- Run **RabbitMQ 4.0.5** with the **Management UI**
- Expose:
  - **RabbitMQ Management UI** → `http://localhost:15672/`
  - **Message Broker (AMQP)** → `amqp://guest:guest@localhost:5672/`
- Create a **virtual host** `/lettuce` with access for the default `guest` user.

#### **Stopping RabbitMQ**
To stop the RabbitMQ container:
```bash
docker-compose -f broker/rabbitmq.yml down
```

### **4️⃣ Install Dependencies**
Clone this repository and install dependencies using **Poetry**:
```bash
git clone https://github.com/daviguides/lettuce-events.git
cd lettuce-events
poetry install
```
This will create and configure a virtual environment with all required dependencies.

### **5️⃣ Running the Services**
#### **Run the Webhook**
To start the webhook server:
```bash
poetry run python webhook.py
```

#### **Or Dispatch an Event**
To send a test event to RabbitMQ:
```bash
poetry run python simple_dispatcher.py
```
This will publish a `payment_created` event.

#### **Run an Event Listener**
Start a worker to listen for an event:
```bash
poetry run python workers/auth_worker.py
poetry run python workers/crm_worker.py
poetry run python workers/logs_payment_worker.py
```
This worker will print all incoming **payment_created** events.

### **6️⃣ Testing the API**
This project includes a `.http` file (`tests/tests.http`) for quick API testing.

#### **📌 API Test File (`tests/tests.http`)**
You can use tools like **Postman**, **VS Code REST Client**, or **HTTPie** to send test requests.

```http
### Test Registration Endpoint

POST http://localhost:8012/registrations HTTP/1.1
Content-Type: application/json

{
    "name": "Davi",
    "birthdate": "1988-12-11"
}


### Test Purchase Endpoint

POST http://localhost:8012/purchases HTTP/1.1
Content-Type: application/json

{
    "product": "Lettuce",
    "quantity": 3,
    "customer": "Davi"
}

### Test Payment Endpoint
POST http://localhost:8012/payments HTTP/1.1
Content-Type: application/json

{
    "customer": "Adan",
    "amount": 1545.95
}
```
#### **How to Run the Tests**
You can test the API using:
- **VS Code REST Client** (Simply open `tests/tests.http` and click "Send Request")
- **HTTPie** (Run `http < tests/tests.http`)
- **Postman** (Import the requests manually)

### **📌 Project Structure**
```
.
├── compose/
│   ├── rabbitmq.yml              # Docker Compose config for RabbitMQ
├── lettuce/
│   ├── __init__.py               # Event-driven abstraction using RabbitMQ
├── tests/
│   ├── tests.http                 # API test file
├── workers/
│   ├── auth_worker.py             # Listens for 'registration_created' events
│   ├── billing_worker.py          # Listens for 'purchase_created' events
│   ├── crm_worker.py              # Listens for 'registration_created' events
│   ├── logs_payment_worker.py     # Logs 'payment_created' events
│   ├── register_payment_worker.py # Handles 'payment_created' events
├── .gitignore
├── LICENSE
├── main.py                        # Main application entry point
├── project.yaml                    # Project configuration
├── pyproject.toml                 # Poetry project configuration
├── README.md                      # Documentation (this file)
├── simple_dispatcher.py           # Sends test events
├── webhook.py                      # Webhook handler
```

### **🔗 References**
- RabbitMQ: [https://www.rabbitmq.com/](https://www.rabbitmq.com/)
- Docker RabbitMQ: [https://hub.docker.com/_/rabbitmq](https://hub.docker.com/_/rabbitmq)
- Poetry Docs: [https://python-poetry.org/docs/](https://python-poetry.org/docs/)
- Blinker Docs: [https://blinker.readthedocs.io/en/stable/](https://blinker.readthedocs.io/en/stable/)
