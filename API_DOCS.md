# Dastavka API Documentation

Suv va shunga o'xshash mahsulotlar dastavkasi uchun RESTful API

## Base URL
```
http://localhost:8000/api/
```

## Authentication
API barcha so'rovlar uchun Token Authentication dan foydalanadi.

### Headers
```
Authorization: Token YOUR_TOKEN_HERE
Content-Type: application/json
```

## API Endpoints

### 1. Authentication
#### Login
- **URL**: `POST /api/users/login/`
- **Body**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```
- **Response**:
```json
{
    "token": "your_token_here",
    "user": {
        "id": 1,
        "username": "your_username",
        "role": "admin"
    }
}
```

#### Logout
- **URL**: `POST /api/users/logout/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Response**: `204 No Content`

### 2. Users Management
#### Get User Profile
- **URL**: `GET /api/users/profile/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Response**:
```json
{
    "id": 1,
    "username": "admin",
    "role": "admin"
}
```

### 3. Client Management

#### List Clients
- **URL**: `GET /api/clients/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `page_size`: Items per page (default: 20)
- **Response**:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "full_name": "John Doe",
            "phone_number": "+998901234567",
            "location_name": "Toshkent",
            "address": "Chilonzor tumani",
            "latitude": 41.2995,
            "longitude": 69.2401,
            "orders_count": 5
        }
    ]
}
```

#### Create Client
- **URL**: `POST /api/clients/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Body**:
```json
{
    "full_name": "John Doe",
    "phone_number": "+998901234567",
    "location_name": "Toshkent",
    "address": "Chilonzor tumani",
    "latitude": 41.2995,
    "longitude": 69.2401
}
```
- **Response**: `201 Created` + client data

#### Get Client Details
- **URL**: `GET /api/clients/{id}/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Response**:
```json
{
    "id": 1,
    "full_name": "John Doe",
    "phone_number": "+998901234567",
    "location_name": "Toshkent",
    "address": "Chilonzor tumani",
    "latitude": 41.2995,
    "longitude": 69.2401,
    "orders_count": 5
}
```

#### Update Client
- **URL**: `PUT /api/clients/{id}/` or `PATCH /api/clients/{id}/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Body**: Same as create (PUT requires all fields, PATCH allows partial)

#### Delete Client
- **URL**: `DELETE /api/clients/{id}/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Response**: `204 No Content`

#### Get Client Orders
- **URL**: `GET /api/clients/{id}/orders/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Response**:
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": "12345",
            "status": "pending",
            "incoming_items": 5,
            "outgoing_items": 3,
            "delivery_date": "2024-01-15",
            "created_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

#### Client Statistics
- **URL**: `GET /api/clients/stats/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Response**:
```json
{
    "total_clients": 25,
    "clients_with_orders": 20,
    "clients_without_orders": 5,
    "top_clients": [
        {
            "id": 1,
            "full_name": "John Doe",
            "orders_count": 15
        }
    ]
}
```

### 4. Orders Management

#### List Orders
- **URL**: `GET /api/orders/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Query Parameters**:
  - `page`: Page number
  - `status`: Filter by status (pending, in_progress, delivered, cancelled)
  - `delivery_date`: Filter by delivery date (YYYY-MM-DD)
- **Response**:
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/orders/?page=2",
    "previous": null,
    "results": [
        {
            "id": "12345",
            "client": {
                "id": 1,
                "full_name": "John Doe",
                "phone_number": "+998901234567",
                "location_name": "Toshkent",
                "address": "Chilonzor tumani",
                "latitude": 41.2995,
                "longitude": 69.2401
            },
            "status": "pending",
            "incoming_items": 5,
            "outgoing_items": 3,
            "delivery_date": "2024-01-15",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        }
    ]
}
```

#### Create Order
- **URL**: `POST /api/orders/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Body**:
```json
{
    "client": {
        "full_name": "John Doe",
        "phone_number": "+998901234567",
        "location_name": "Toshkent",
        "address": "Chilonzor tumani",
        "latitude": 41.2995,
        "longitude": 69.2401
    },
    "incoming_items": 10,
    "outgoing_items": 0,
    "delivery_date": "2024-01-20"
}
```
- **Response**: `201 Created` + order data

#### Get Order Details
- **URL**: `GET /api/orders/{id}/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Response**: Same format as list item

#### Update Order
- **URL**: `PUT /api/orders/{id}/` or `PATCH /api/orders/{id}/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Body**: Same as create (PUT requires all fields, PATCH allows partial)

#### Delete Order
- **URL**: `DELETE /api/orders/{id}/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Response**: `204 No Content`

#### Order Statistics
- **URL**: `GET /api/orders/stats/`
- **Headers**: `Authorization: Token YOUR_TOKEN`
- **Response**:
```json
{
    "total_orders": 100,
    "pending_orders": 25,
    "in_progress_orders": 15,
    "delivered_orders": 55,
    "cancelled_orders": 5,
    "today_orders": 8
}
```

## Status Codes

- `200 OK`: Successful GET, PATCH, PUT requests
- `201 Created`: Successful POST requests
- `204 No Content`: Successful DELETE requests
- `400 Bad Request`: Invalid data sent
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Order Statuses

- `pending`: Yangi buyurtma
- `in_progress`: Jarayonda
- `delivered`: Yetkazilgan
- `cancelled`: Bekor qilingan

## Order ID System

Buyurtma ID'lari avtomatik generatsiya qilinadi:
- 5 xonali ID'lar: 10000-99999
- Agar 5 xonali ID'lar tugasa, avtomatik 6 xonaliga o'tadi: 100000-999999
- ID collision detection va retry mechanism mavjud

## Error Responses

```json
{
    "error": "Error message here",
    "details": {
        "field_name": ["Field specific error message"]
    }
}
```

## API Schema

Avtomatik generatsiya qilingan API schema:
- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

## Examples

### Complete Workflow Example

1. **Login**:
```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

2. **Create Client**:
```bash
curl -X POST http://localhost:8000/api/clients/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "full_name": "Ahmad Karimov",
    "phone_number": "+998901234567",
    "location_name": "Toshkent",
    "address": "Mirzo Ulug'bek tumani",
    "latitude": 41.2995,
    "longitude": 69.2401
  }'
```

3. **Create Order**:
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{
    "client": {
      "full_name": "Ahmad Karimov",
      "phone_number": "+998901234567",
      "location_name": "Toshkent",
      "address": "Mirzo Ulug'bek tumani",
      "latitude": 41.2995,
      "longitude": 69.2401
    },
    "incoming_items": 15,
    "outgoing_items": 0,
    "delivery_date": "2024-01-20"
  }'
```

4. **Get Orders**:
```bash
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Token YOUR_TOKEN"
```

## Notes

- Barcha vaqt ma'lumotlari UTC formatida
- Telefon raqamlari international formatda (+998xxxxxxxxx)
- GPS koordinatalari decimal format (latitude, longitude)
- Pagination barcha list endpoint'larida mavjud
- Client ma'lumotlari order yaratishda avtomatik yaratiladi yoki mavjudiga ulanadi