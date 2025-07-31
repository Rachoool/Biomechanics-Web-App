# 📘 BioData Viewer - Living API Documentation

## 🔧 Overview

This document serves as the **living backend API documentation** for the BioData Viewer project. It is automatically maintained using Swagger/OpenAPI and reflects the latest status of all exposed endpoints. All API changes must be updated here and reviewed via pull requests.

---

## 📐 API Design Principles

- **Contract-First**: APIs are designed and agreed upon before implementation to align frontend and backend.
- **RESTful Architecture**: Consistent HTTP verbs, paths, and status codes.
- **Versioning**: Future support for `/api/v1/` style versioning.
- **OpenAPI-based Documentation**: Served through Swagger UI.

---

## 🌐 Base URL

- Development: `http://localhost:5000/api/`
- Production: `https://<your-domain>.com/api/`

---

## 🧾 API Endpoints

### `GET /api/hello`

- **Purpose**: Test backend availability.
- **Response**:
  ```json
  {
    "message": "Hello from Flask!"
  }

## POST /api/upload

### Purpose
Upload one or more 3D models or medical image files.

### Accepted File Types
`.stl`, `.obj`, `.dcm`, `.nii`

### Request Type
`multipart/form-data`

### Request Field
- `files`: one or more files to be uploaded

---

- **Good Response**:
  ```json
  {
    "status": "success",
    "filenames": ["example.stl"]
  }

- **Bad Response**:
  ```json
  {
    "status": "error",
    "message": "No valid files uploaded"
  }

### `GET /api/models`

- **Purpose**: List available 3D model files.
- **Response**:
  ```json
  {
    "models": ["femur.stl", "knee.obj"]
  }

### `GET /uploads/<filename>`

- **Purpose**: Serve uploaded model files for rendering.

### `DELETE /api/delete/<filename>`

- **Purpose**: Delete a model file from server.
- **Response**:
  ```json
  {
    "status": "success",
    "message": "example.obj deleted"
  }

- **Error**:
  ```json
  {
    "status": "error",
    "message": "File not found"
  }


## 🛠️ Error Handling Conventions

| HTTP Code | Message         | Description                      |
|-----------|------------------|----------------------------------|
| 200       | success          | Request completed successfully   |
| 400       | error            | Invalid request or missing data  |
| 404       | File not found   | Target file does not exist       |
| 500       | Internal error   | Unexpected backend failure       |

