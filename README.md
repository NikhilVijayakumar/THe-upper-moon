# 🗡️ HashiraMart AI System Documentation

### *AI Weapon Recommender • AI Combat Coach • MLOps • Generative Slayer Visualization*

---

## ⚔️ 1. Overview

**HashiraMart** is an AI-driven E-commerce platform designed for *Demon Slayers* to discover, train, and master their perfect weapons.
Unlike a traditional e-commerce store, HashiraMart merges **AI recommendations**, **personalized coaching**, and **immersive visuals** to form a **living dojo experience**.

This documentation covers the **full technical design**, including:

* AI Weapon Recommender (Recommender System)
* AI Combat Coach (LLM-based Training Companion)
* End-to-End MLOps Pipeline (DVC + MLflow + Git)
* Web UI + FastAPI Backend
* Database Design & Gamification Engine
* Generative AI Visualization (Slayer with weapon image synthesis)

---

## 🧠 2. System Architecture Overview

```plaintext
            ┌────────────────────────────────────┐
            │            Web UI (React)          │
            │  - RecommenderView                │
            │  - CombatCoachChat                │
            │  - Image Preview (Generative)     │
            └──────────────┬────────────────────┘
                           │
                           ▼
                ┌──────────────────────┐
                │ FastAPI Backend      │
                │  /recommend          │
                │  /coach/chat         │
                │  /generate_image     │
                │  /events             │
                └────────┬─────────────┘
                         │
 ┌────────────────────────────────────────────────────┐
 │ MLOps Pipeline                                     │
 │ ├── DVC for dataset & model versioning              │
 │ ├── MLflow for experiment tracking & model registry │
 │ └── Git for code versioning                         │
 └────────────────────────────────────────────────────┘
                         │
                         ▼
          ┌──────────────────────────────┐
          │ Database (Postgres)          │
          │  - slayers                   │
          │  - weapons                   │
          │  - interactions              │
          │  - gamification              │
          └──────────────────────────────┘
                         │
                         ▼
         ┌─────────────────────────────┐
         │ Generative Image System     │
         │  (Stable Diffusion / API)   │
         │  Generates Slayer+Weapon Img│
         └─────────────────────────────┘
```

---

## ⚙️ 3. AI Weapon Recommender

### Purpose

Predicts which weapon best suits a Slayer based on their profile (skills, breathing style, past battles) and weapon features.

### Workflow

1. **Synthetic Dataset Generation**

   * Simulated profiles, weapons, and combat results (`success` metric)
   * Stored under `data/raw/` and tracked with DVC.

2. **Feature Engineering**

   * Combines Slayer and weapon data.
   * Adds derived features such as:

     * `match_style` (breathing compatibility)
     * `level_weight_diff`
     * `strength`, `dexterity`, `stamina` scores

3. **Model Training**

   * **LightGBM** used to train a binary classifier predicting “combat success.”
   * Logged to **MLflow** for version tracking and performance monitoring.

4. **Output**

   * Ranked weapon recommendations for each Slayer (`top_k` predictions).

### Example Features

| Feature                        | Description                               |
| ------------------------------ | ----------------------------------------- |
| level                          | Slayer experience level                   |
| strength / dexterity / stamina | Physical attributes                       |
| weight / sharpness             | Weapon attributes                         |
| match_style                    | 1 if breathing style matches weapon type  |
| price                          | Cost (used for balancing recommendations) |

---

## 🔁 4. MLOps Pipeline (DVC + MLflow + Git)

### Pipeline Flow

| Stage               | Tool              | Description                    |
| ------------------- | ----------------- | ------------------------------ |
| `generate_data`     | Python + DVC      | Create synthetic dataset       |
| `train_recommender` | LightGBM + MLflow | Train & log model              |
| `evaluate`          | MLflow            | Track metrics (AUC, accuracy)  |
| `deploy`            | Git + FastAPI     | Deploy latest production model |

### Example `dvc.yaml`

```yaml
stages:
  generate_data:
    cmd: python src/dataset/generate_synthetic.py
    outs:
      - data/raw/
  train_recommender:
    cmd: python src/models/train_recommender.py
    deps:
      - data/raw/
      - src/models/train_recommender.py
    outs:
      - model/lgb_model.pkl
```

### Example MLflow Experiment

```python
mlflow.set_experiment("weapon-recommender")
with mlflow.start_run():
    ...
    mlflow.lightgbm.log_model(model, "lgb_model")
    mlflow.log_metric("auc", auc_score)
```

### Versioning

* **Code:** Git
* **Data:** DVC
* **Model:** MLflow
* **Params:** YAML config files (`params.yaml`)

---

## 🧩 5. AI Combat Coach

### Purpose

Acts as a **virtual mentor** to Slayers, providing:

* Weapon handling tips
* Training drills
* Maintenance routines
* Motivation and gamified feedback

### Design

| Component       | Description                                          |
| --------------- | ---------------------------------------------------- |
| LLM Core        | GPT / LLaMA / Mistral model for context-aware advice |
| Context Adapter | Injects weapon data, user profile, and history       |
| Chat Interface  | Web-based chat UI for two-way communication          |
| Feedback Loop   | Logs interactions and feeds data back into training  |

### Prompt Example

> “You are the AI Combat Coach for HashiraMart.
> The user uses Water Breathing and owns a Rare Katana.
> Provide a 5-minute daily routine and one motivational quote.”

### Integration with E-commerce

* Post-purchase assistant for training.
* Increases engagement, retention, and upselling (e.g., accessories).

---

## 🧱 6. Backend (FastAPI)

### Endpoints

| Endpoint               | Description                             |
| ---------------------- | --------------------------------------- |
| `POST /recommend`      | Returns top weapon recommendations      |
| `POST /coach/chat`     | Returns AI coaching advice              |
| `POST /events`         | Logs interactions, updates gamification |
| `POST /generate_image` | Generates a Slayer+weapon image         |

### Example Code

```python
@app.post("/recommend")
def recommend(req: RecommendRequest):
    slayer = fetch_slayer(req.slayer_id)
    weapons = fetch_weapons()
    X = featurize(slayer, weapons)
    preds = model.predict_proba(X)[:,1]
    return sorted(zip(weapons, preds), key=lambda x: x[1], reverse=True)[:req.top_k]
```

---

## 🧮 7. Database Design (PostgreSQL)

### Tables

| Table          | Description                         |
| -------------- | ----------------------------------- |
| `slayers`      | Stores user profiles                |
| `weapons`      | Weapon inventory and attributes     |
| `interactions` | Battle outcomes (for training data) |
| `gamification` | Points and ranks                    |

### Example Schema

```sql
CREATE TABLE slayers (
  id UUID PRIMARY KEY,
  name TEXT,
  breathing_style TEXT,
  level INT,
  strength FLOAT,
  dexterity FLOAT,
  stamina FLOAT
);

CREATE TABLE gamification (
  slayer_id UUID PRIMARY KEY,
  nichirin_points INT DEFAULT 0,
  rank TEXT DEFAULT 'Apprentice'
);
```

---

## 🕹️ 8. Gamification Engine (PoC)

### Points Logic

| Event                          | Points |
| ------------------------------ | ------ |
| Successful Battle              | +10    |
| Training Activity (per 10 min) | +1     |
| Daily Login Streak             | +5     |

### Rank Tiers

| Tier       | Points Required |
| ---------- | --------------- |
| Apprentice | 0–99            |
| Slayer     | 100–499         |
| Hashira    | 500+            |

---

## 💻 9. Web UI (React)

### Components

| Component         | Description                     |
| ----------------- | ------------------------------- |
| `RecommenderView` | Displays top weapon suggestions |
| `CombatCoachChat` | Chat interface with AI Coach    |
| `ImagePreview`    | Displays generated Slayer image |
| `Dashboard`       | Shows profile, points, rank     |

### Example (Weapon Recommender)

```jsx
<button onClick={fetchRecs} className="btn">Suggest Weapons</button>
<ul>
  {recs.map(r => (
    <li key={r.weapon_id}>
      {r.weapon_id} - Score: {r.score.toFixed(2)}
    </li>
  ))}
</ul>
```

---

## 🧬 10. Generative Image Module

### Purpose

Replaces AR Tryout Zone by generating **custom AI art** of the Slayer wielding their chosen weapon.

### Tools

* **Stable Diffusion (via diffusers)**
* Optionally integrate **ControlNet** for pose control or **Replicate API** for hosted inference.

### Example Code

```python
def generate_slayer_image(name, breathing_style, weapon_type):
    prompt = f"{name}, {breathing_style} Breathing, wielding a {weapon_type}, anime style, cinematic"
    image = pipe(prompt, guidance_scale=7.5).images[0]
    image.save(f"out/{name}_{weapon_type}.png")
```

---

## 🔄 11. Model Retraining Loop

1. Collect new interactions from `/events`
2. Append to `data/raw/interactions.csv`
3. Trigger nightly retraining:

   ```bash
   dvc repro
   ```
4. Track metrics in MLflow
5. Promote best-performing model to production tag
6. FastAPI reloads latest model automatically

---

## 🧩 12. Tech Stack Summary

| Layer            | Technology             |
| ---------------- | ---------------------- |
| Frontend         | React + Tailwind       |
| Backend          | FastAPI                |
| Database         | PostgreSQL             |
| ML Models        | LightGBM + LLM (Coach) |
| MLOps            | DVC + MLflow + Git     |
| Visualization    | Stable Diffusion       |
| Containerization | Docker + Compose       |

---

## 🚀 13. Deployment & Runbook

### Local Dev Setup

```bash
git clone <repo>
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
dvc pull
uvicorn src.api.app:app --reload
cd src/webui/react-app && npm run dev
```

### Docker Compose Services

* `backend` → FastAPI app
* `db` → PostgreSQL
* `mlflow` → Experiment tracker
* `frontend` → React app

---

## 🧱 14. Future Enhancements

* 🎯 **Real-time Demon Threat Prediction** (geolocation-based)
* 🧩 **Voice Command Coach** (“Train me for Water Breathing”)
* 💰 **Dynamic Weapon Pricing AI** (based on demand)
* ⚙️ **CrewAI Integration** for modular agents
* 🖼️ **Slayer NFT / digital certificate generation**

---

## 🩸 15. Tagline

> *“Every Slayer deserves their perfect blade — forged by AI, sharpened through training.”*

---



Would you like me to now **generate a folder structure and initial files** (`src/`, `dvc.yaml`, `train_recommender.py`, etc.) in Markdown tree form so you can copy it directly into your repo?
