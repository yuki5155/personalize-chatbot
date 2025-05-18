"""
Cookieベースの認証をテストするためのクライアント
"""
import requests

BASE_URL = "http://localhost:8000"

def test_cookie_auth():
    """
    Cookieベースの認証フローをテストします
    """
    # ステップ1: クッキーなしでアクセスするとエラーになることを確認
    print("\n1. クッキーなしでアクセス（エラーになるはず）:")
    try:
        response = requests.get(f"{BASE_URL}/users/me")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"エラー: {e}")

    # ステップ2: Cookieを設定
    print("\n2. ユーザーIDをCookieに設定:")
    user_id = "1"  # admin ユーザー
    response = requests.get(f"{BASE_URL}/users/set-cookie/{user_id}")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")
    cookies = response.cookies

    # ステップ3: 設定したCookieでアクセス
    print("\n3. 設定したCookieでアクセス（成功するはず）:")
    response = requests.get(f"{BASE_URL}/users/me", cookies=cookies)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")

    # ステップ4: 存在しないユーザーIDでのテスト
    print("\n4. 存在しないユーザーIDでテスト（エラーになるはず）:")
    invalid_response = requests.get(f"{BASE_URL}/users/set-cookie/999")
    invalid_cookies = invalid_response.cookies
    response = requests.get(f"{BASE_URL}/users/me", cookies=invalid_cookies)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.json()}")


if __name__ == "__main__":
    test_cookie_auth() 