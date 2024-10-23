# Solana Assest

Web challenge where you have to get the flag with an cookie which contains a flag **Level**:Easy

---

## Concept 

## Challenge Overview:

    - The attacker needs to retrieve a flag from a web application. The flag is stored in a cookie named flag, but it is dynamically generated. The attacker has to perform actions on the web application to get access to the flag stored in the cookie.

    - The challenge includes typical security protections, like HTTP-only cookies or obfuscation, that the attacker needs to bypass.

---

### Web Application:

    A simple web app with two pages:
        Login Page (/login): Users can log in with a specific username (admin) and password.
        Dashboard Page (/dashboard): Once logged in, users are directed to the dashboard, and a cookie named flag is set. The cookie contains the dynamically generated flag, but it's not immediately accessible through client-side JavaScript (i.e., it's set as HTTP-only).

### Cookie Properties:

    The flag cookie should have the following properties:
        HTTP-only: Prevents access to the flag via JavaScript.
        Secure: Ensures that the cookie is only sent over HTTPS.
        Dynamic: The flag is unique per session, generated during the login process.

### Docker Environment:

    The web server (e.g., Flask, Express.js, or PHP) runs inside a Docker container.
    A simple Docker Compose setup with a web container running the web app.

> [!IMPORTANT]
> Flags are dynamically created in the backend for each team.

---


## Attack Paths:

    **XSS Attack:** If the application has an XSS vulnerability, the attacker can inject malicious JavaScript to exploit the session of a legitimate user and steal their cookie.

    **Session Hijacking:** By figuring out how the session or login mechanism works, the attacker can potentially steal a session or manipulate their session to retrieve the cookie.

    **Cookie Replay:** The attacker might try to replay a valid login session and retrieve the flag cookie by inspecting network traffic.

