import pytest
from app.validators.sql_validator import SQLValidator
from app.core.exceptions import UnsafeSQLException


def test_valid_select_query():
    validator = SQLValidator()
    assert validator.validate("SELECT * FROM users") is True


def test_valid_with_query():
    validator = SQLValidator()
    assert validator.validate("WITH cte AS (SELECT * FROM users) SELECT * FROM cte") is True


def test_blocked_drop_query():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("DROP TABLE users")


def test_blocked_delete_query():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("DELETE FROM users WHERE id=1")


def test_blocked_truncate_query():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("TRUNCATE TABLE users")


def test_blocked_alter_query():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("ALTER TABLE users ADD COLUMN name TEXT")


def test_blocked_update_query():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("UPDATE users SET name='test' WHERE id=1")


def test_blocked_insert_query():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("INSERT INTO users (name) VALUES ('test')")


def test_blocked_create_query():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("CREATE TABLE test (id INT)")


def test_blocked_grant_query():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("GRANT SELECT ON users TO test_user")


def test_blocked_revoke_query():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("REVOKE SELECT ON users FROM test_user")


def test_blocked_exec_query():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("EXEC sp_help")


def test_blocked_keyword_in_middle():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("SELECT * FROM users WHERE name='drop'")


def test_case_insensitive_block():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("delete from users")


# Prompt Injection & Malicious Query Tests
def test_prompt_injection_ignore_previous():
    validator = SQLValidator()
    # Even with "ignore previous instructions", the SQL is still checked
    sql = "SELECT * FROM users; DROP TABLE users"
    with pytest.raises(UnsafeSQLException):
        validator.validate(sql)


def test_malicious_query_semicolon():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("SELECT * FROM users; DELETE FROM users")


def test_malicious_query_comment():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("SELECT * FROM users --; DROP TABLE users")


def test_malicious_query_union():
    validator = SQLValidator()
    # Union is okay, but if it has malicious keywords, block
    with pytest.raises(UnsafeSQLException):
        validator.validate("SELECT * FROM users UNION SELECT * FROM users; DROP TABLE users")


def test_valid_complex_select():
    validator = SQLValidator()
    assert validator.validate("""
        SELECT 
            u.id,
            u.name,
            COUNT(o.id) AS order_count
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        WHERE u.active = 1
        GROUP BY u.id, u.name
        HAVING COUNT(o.id) > 5
        ORDER BY order_count DESC
        LIMIT 10
    """) is True


def test_blocked_execute():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("EXECUTE('DROP TABLE users')")


def test_blocked_keyword_in_subquery():
    validator = SQLValidator()
    with pytest.raises(UnsafeSQLException):
        validator.validate("SELECT * FROM (DELETE FROM users)")

