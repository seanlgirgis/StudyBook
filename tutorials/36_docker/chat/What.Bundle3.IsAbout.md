Exactly — this is where Docker stops being “images” and becomes a **real system**.

---

# 🧠 What Bundle 03 is about

> “Run multiple containers together as one application.”

Instead of:

```text
1 container → 1 script
```

You’ll run:

```text
App + Database + (maybe cache) → working system
```

---

# 🧱 The tool: Docker Compose

You’ll use:

👉 `docker compose`

Which lets you define everything in one file:

```yaml id="h03s9l"
services:
  app:
    build: .
  db:
    image: postgres:15
```

---

# 🧠 Mental model

![Image](https://images.openai.com/static-rsc-4/KVKpe9hz7NWfKF4-s68GVbjHceeJTO7uyyodDzaiu7O1Z1JEGyqFCr22GtRjhN40ikujyb-LpBV6QBTkZ61jrzG3nc4USqkeILBWgN5uMp8_6ihuKjeMZZXbYl0_H8WtO6In0t_GTISbuiVKz2kxbtpWrqTNq-vM1bFtOrkdjyrnMw1B8_iqwKLoVVec8zZP?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/9dVxbkB2JP1Q3oJPOE2KLc-QVOCtpQ1tBpgNmQcvEMPLDUiyS3Gefh83EkzWxT870uaTUd8CodRDgpDKEwD9S74lD8LW_b2cd7t_wsizYzZFyEe1yGsk_DuasaWBVVpev7Z8ubbJhtCs7JYGttT6fQDJExlmmClPQtKHALlB4zkctv2F9_u_jv497nzFl9_Z?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/olVpsut9voLRrN3yDYe1HY_rRPFXt0foya92W-MaSZxHYgCM_lYgN5x3B-jF8sm1OkOv3K-ywsraj1obuVDfglXJ0dWOvzbEubPjIsNV9f5egyjLgBNGghYPY9zHVhbwVk2qM4_p9wbyMOJ7LveTMPJ7444Cs2Pp_4k8LfDoWpxh1D917_s_5UOh1b92yRGR?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/cP_IDdGkMZtXfhET76aBzxl0N39_1AFLfLZIbZV8bT8_7QRFv_fZvjJTAKPX-rtFfL8VKINxMBChidkRyWh0QOesCb_nsok9XmgjpeIGlLI1JKKdp2I77BBNkJeXNG_L6damJnOoNwsnwdd_i6-igQrIfQny9U9nDv7EuRc-GNowxXUOleI8j6mi6hA2jhB-?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/8PPKXSyUaxkpNjehHx13DUlaE1fHfferv6B4kEBwNDJVwj7ovtBNQG-FVw3Mn2DSZMBzKAdPlZwfWraw6YPiewHDxRr8qH5QhSxMaPRNXMTLUt6EzpycIjWwt_Ez5VbgI1J3lRoPaPFHy436jfUyyt6iS-PuYEAWfJElf_vTWA1-mNbJZktCcEppPIZktG9m?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/8nyQUsy6mJMYLkl36KIZDsQuTF1EMXq9HBqkFPXx5XHVYIzgM-nW6UPvaUGqyKQI5dVwksdREnJaQp-IPJEVfOkvJXKwUG2qEEW3uHdynaxX4S8KwpyQutsmkwFpG4CbWVCZ97eXW90LWNIr8PoCrx0ak96eAA76IJxl1dxRRpJr4KeEsN2HUp4SnNZjUbW1?purpose=fullsize)

* Each service = one container
* They talk over a private network
* Compose manages them together

---

# ⚙️ What Bundle 03 will introduce

### 1. Multiple services

* `app` → your pipeline
* `db` → Postgres

---

### 2. Networking (automatic)

Containers can talk like:

```text
app → db:5432
```

No IP setup needed.

---

### 3. Volumes (data persistence)

Database data survives restarts.

---

### 4. One command to run everything

```bash id="l0r7r1"
docker compose up --build
```

---

### 5. One command to stop everything

```bash id="9h4m0f"
docker compose down
```

---

# 🔥 What this means in real life

You’re now doing what teams actually do:

* Backend service
* Database
* Worker jobs

All running together locally exactly like production

---

# 🧪 What you’ll *see*

When you run:

```bash id="mz4p4v"
docker compose up
```

You’ll see:

```text
app-1  | Starting pipeline...
db-1   | PostgreSQL starting...
```

👉 Multiple containers running at once

---

# 🔍 Check it live

```bash id="g7b4ha"
docker ps
```

👉 You’ll finally see:

* multiple running containers

---

# ⚡ One-line summary

> “Docker Compose lets me run a full system of containers with one command.”

---

# 🚀 Before we generate Bundle 03

Quick check — do you want:

### Option A (recommended)

👉 **App + Postgres (realistic data pipeline)**

### Option B

👉 Simple multi-container demo (lighter)

---

Say:
👉 **A** or **B**

and I’ll generate Bundle 03 exactly like your previous bundles.
