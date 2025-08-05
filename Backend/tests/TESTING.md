# TESTING

## 1. Framework
The backend is tested using **pytest**.  
Version used: `pytest 8.4.1`  

Run tests from the project **root**:
```bash
python -m pytest Backend/tests --disable-warnings -v
```

## 2. Scope
The test suite covers the following backend API endpoints:

- **`GET /api/hello`**  
  - Checks if the server responds with status `200` and the correct JSON message.

- **`POST /api/upload` & `GET /api/models`**  
  - Uploads a valid `.stl` file and verifies it appears in the models list.

- **`POST /api/upload` with invalid file**  
  - Uploads an unsupported file type (e.g., `.txt`) and expects status `400`.

- **`DELETE /api/delete/<filename>`**  
  - Deletes an existing file and expects status `200`.  
  - Deletes a non-existing file and expects status `404`.

## 3. Implementation
**Fixtures:**
- `client`: Flask test client for simulating API requests.
- `tmp_path`: Temporary directory for storing uploaded files during tests.

**Monkeypatching:**
- The `UPLOAD_FOLDER` path in `app.py` is patched to `tmp_path` to ensure test isolation.

---

## 4. Results
All tests executed successfully.

| Test Case                               | Status |
|-----------------------------------------|--------|
| `test_hello`                            |  Pass  |
| `test_upload_and_list_models`           |  Pass  |
| `test_upload_invalid_file`              |  Pass  |
| `test_delete_file`                      |  Pass  |
| `test_delete_nonexistent_file`          |  Pass  |

**Summary:** 5 tests run, all passed in 0.35s.
