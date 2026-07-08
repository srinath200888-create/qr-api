# RapidAPI Listing Guide - QR Code API

## Step 1: Deploy to Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repo: `srinath200888-create/qr-api`
4. Render will auto-detect `render.yaml` and deploy
5. Wait for the deploy to finish (2-3 min)
6. Your API URL will be: `https://qr-api.onrender.com`

### Environment Variables (set in Render dashboard):
| Variable | Value |
|---|---|
| `RAPIDAPI_ENABLED` | `true` |
| `RATE_LIMIT_ENABLED` | `true` |

---

## Step 2: Create RapidAPI Provider Account

1. Go to https://rapidapi.com and sign up / log in
2. Click your profile icon → "My APIs"
3. Click "Add New API"

---

## Step 3: API Configuration on RapidAPI

### Basic Info
| Field | Value |
|---|---|
| **API Name** | QR Code API |
| **Description** | Generate customizable QR codes with colors, embedded logos, custom sizes, and multiple formats (PNG, SVG). Perfect for marketing, events, product packaging, and digital signage. |
| **Category** | Tools |
| **Visibility** | Public |
| **Base URL** | `https://qr-api.onrender.com/v1` |

### Endpoints to Add

#### 1. POST /generate
- **Summary**: Generate QR code
- **Description**: Generate a QR code from text or URL. Returns the image directly.
- **Request Format**: `application/json`
- **Parameters**:

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | ✅ | - | Text or URL to encode (1-2000 chars) |
| `size` | integer | ❌ | 200 | Image size in pixels (50-4096) |
| `color` | string | ❌ | #000000 | Foreground hex color |
| `bg_color` | string | ❌ | #FFFFFF | Background hex color |
| `format` | string | ❌ | png | Output: `png` or `svg` |
| `logo` | string | ❌ | null | Base64-encoded logo image |

- **Response**: Binary image (`image/png` or `image/svg+xml`)
- **Error Response**: `{"success": false, "error": "message"}`

#### 2. POST /generate/bulk
- **Summary**: Generate multiple QR codes
- **Description**: Generate up to 100 QR codes in one request. Returns base64-encoded images.
- **Request Format**: `application/json`
- **Parameters**:

| Param | Type | Required | Default | Description |
|---|---|---|---|---|
| `items` | array | ✅ | - | Array of QR items (1-100) |
| `format` | string | ❌ | png | Output format for all items |

**Item Object:**
| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `text` | string | ✅ | - | Text or URL to encode |
| `size` | integer | ❌ | 200 | Image size |
| `color` | string | ❌ | #000000 | Foreground color |
| `bg_color` | string | ❌ | #FFFFFF | Background color |
| `logo` | string | ❌ | null | Base64 logo |

- **Response**: `{"success": true, "data": [{"index": 0, "qr": "base64...", "error": null}]}`

#### 3. GET /health
- **Summary**: Health check
- **Description**: Check if the API is running
- **Response**: `{"status": "ok", "version": "1.0.0"}`

---

## Step 4: Pricing Plans (Recommended)

RapidAPI supports **included requests + overage pricing**. Here's the recommended setup:

### Free Plan - $0/mo
| Setting | Value |
|---|---|
| Included Requests | 3,000 / month (~100/day) |
| Additional Request | N/A (hard cap) |
| Rate Limit | 100 req/day |
| Features | Basic QR, up to 500px size |

### Basic Plan - $9.99/mo
| Setting | Value |
|---|---|
| Included Requests | 50,000 / month |
| Additional Request | $0.0005/req ($0.50 per 1K extra) |
| Features | Custom colors, up to 1024px size |

### Pro Plan - $29.99/mo
| Setting | Value |
|---|---|
| Included Requests | 300,000 / month |
| Additional Request | $0.0003/req ($0.30 per 1K extra) |
| Features | Custom colors, logo embedding, up to 2048px size, SVG output |

### Ultra Plan - $99.99/mo
| Setting | Value |
|---|---|
| Included Requests | 1,000,000 / month |
| Additional Request | $0.0001/req ($0.10 per 1K extra) |
| Features | All features, up to 4096px size, priority support, bulk generation |

---

## Step 5: Security Setup

1. In your RapidAPI provider dashboard, generate a **Proxy Secret**
2. Set it as an environment variable in Render:
   ```
   RAPIDAPI_SECRET=your_proxy_secret_here
   ```
3. This ensures only RapidAPI-proxied requests reach your backend

---

## Step 6: Test Before Publishing

Use RapidAPI's built-in testing console to test:
- `POST /generate` with `{"text": "https://example.com"}`
- `POST /generate` with `{"text": "hello", "color": "#FF0000", "bg_color": "#000000"}`
- `POST /generate/bulk` with 2-3 items
- `GET /health`

---

## Quick Revenue Math

If 100 users on Basic ($9.99) + 20 on Pro ($29.99) + 5 on Ultra ($99.99):

```
100 × $9.99   =   $999
 20 × $29.99  =   $600
  5 × $99.99  =   $500
 ---------------------
Total:         $2,099/mo
```

Plus overage revenue on top. Operating cost on Render free tier: **$0**.

---

## OpenAPI Spec

An `openapi.yaml` file is included in the repo. You can import this into RapidAPI during the "Add New API" process for automatic endpoint configuration.
