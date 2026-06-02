# Pa Rang Cafe & Art Stay — Premium Static Website

Welcome to your brand-new, high-aesthetic, static website for **Pa Rang Cafe & Art Stay** in Chiang Mai, Thailand! 

This website has been built to be **extremely low-maintenance**, blazing fast, responsive, and beautiful. It is composed of a single, masterfully designed, long-scroll page that works natively in all web browsers without any complex compiler scripts, Jekyll dependencies, or databases.

---

## 📸 Real-World Enhanced Photos & Live Social Feeds

To give you the absolute best of both worlds, the website blends **premium-grade, AI-color-enhanced real photographs of your space** alongside **real-time social proof**:

### A. Color-Enhanced Core Highlights
We have taken your actual uploaded photos and enhanced their color, contrast, and presentation using an AI Image Enhancer, elevating them to a premium curatorial standard. They are located inside the `assets/images/` directory:
* **Garden Facade / Space image** (Hero backdrop & About): `real_hero_garden.png` (Enhanced from `house1.jpg`)
* **Cozy Boutique Rooms image** (Stay card 1): `real_stay_room.png` (Enhanced from `room3.jpg`)
* **Cafe Smoothies & Drinks image** (Cafe section): `real_cafe_drinks.png` (Enhanced from `drink1.jpg`)
* **Terracotta Clay Workshops in Action** (Events Card 1): `real_terracotta.png` (Enhanced from `terracotta.jpg`)

### B. Authentic Event Snapshots
In addition to the enhanced highlights, the happenings grid integrates your actual, raw photos to show real people, real workshops, and real concerts:
* **Garden Music Nights:** `garden music.jpg`
* **Community Suppers:** `garden socializing.jpg`
* **Artist Talks & Studio Tours:** `indigoworkshop.jpg`

### C. Ever-Green Social Portal
* **Instagram & Facebook Portals:** We have styled a premium, minimalist **"See What's Happening This Week"** call-to-action box directly under your workshop grid. This links visitors instantly to your live accounts (`@parang_cnx` on Instagram and `/parangcafe` on Facebook) where they can view your real-time calendars, flyers, and fresh weekly updates, completely bypassing high-maintenance iframe widgets!

---

## 📂 Project Structure

All your website files are neatly organized in the root folder:

```text
├── index.html                # The main single-page website code (HTML5 + JS)
├── assets/
│   ├── css/
│   │   └── style.css         # All visual styles, typography, and theme (CSS3)
│   └── images/               # Put your favorite REAL JPEGs in this folder!
│       ├── real_hero_garden.png  # Enhanced garden courtyard facade
│       ├── real_stay_room.png    # Enhanced interior boutique room
│       ├── real_cafe_drinks.png  # Enhanced frothy garden latte
│       ├── real_terracotta.png   # Enhanced terracotta workshop image
│       ├── garden music.jpg      # Live garden acoustic session
│       ├── garden socializing.jpg# Socializing nooks in garden
│       ├── indigoworkshop.jpg    # Blue indigo-dyeing craft workshop
│       └── ...                   # Other raw JPEG assets from your phone!
└── README.md                 # This documentation guide
```

---

## 🛠️ How to Edit & Update Content

You do **not** need any coding experience to update this site. Simply open `index.html` in a plain text editor (like VS Code, Sublime Text, TextEdit, or Notepad) and change the text between the HTML tags.

Here are the most common things you might want to edit:

### 1. Booking Links (Airbnb & Booking.com)
If your Airbnb or Booking.com links change, search `index.html` for `Booking.com` or `Airbnb` and update the `href="..."` attribute inside the link tags:
* **Booking.com (Cozy Rooms)** is around **Line 288**:
  ```html
  <a href="YOUR_NEW_BOOKING_LINK" target="_blank" ...>Book a Room on Booking.com</a>
  ```
* **Airbnb (Entire compound)** is around **Line 310**:
  ```html
  <a href="YOUR_NEW_AIRBNB_LINK" target="_blank" ...>Book Entire Compound on Airbnb</a>
  ```

### 2. The Cafe Menu Highlights
To change the drink highlights, search `index.html` for `<div class="menu-highlight-list">` (around **Line 227**). You will see items like this:
```html
<div class="menu-item">
  <h4>Mango Passion Tropical Smoothie</h4> <!-- Edit name here -->
  <span>Refreshing</span>                  <!-- Edit tag here -->
</div>
```
Simply edit the text inside `<h4>` and `<span>`.

### 3. Contact Details & Open Hours
To update the contact panel or map, scroll to the bottom of `index.html` around **Line 397** (`<section id="contact" ...>`). You can modify:
* The street address
* The daily cafe opening hours
* The contact email address (`parang.cnx@gmail.com`)

---

## 🚀 How to Host on GitHub Pages (Free)

Hosting this static site on **GitHub Pages** is completely free, secure, and takes less than 2 minutes to set up.

### Step 1: Upload Your Code to a GitHub Repository
1. Log in to your account at [github.com](https://github.com).
2. Click **New Repository** (green button).
3. Name your repository (e.g., `parang-cnx`). Keep it **Public**.
4. Do not initialize with a README, `.gitignore`, or License.
5. In your local terminal inside this folder, run:
   ```bash
   git init
   git add .
   git commit -m "Initial launch of Pa Rang website"
   git branch -M main
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/parang-cnx.git
   git push -u origin main
   ```

### Step 2: Turn on GitHub Pages
1. Go to your repository on GitHub.com.
2. Click on the **Settings** tab (the gear icon on the top right).
3. In the left-hand sidebar, scroll down to the **Code and automation** section and click **Pages**.
4. Under **Build and deployment**:
   * **Source:** Select **Deploy from a branch**.
   * **Branch:** Select `main` (or `master`) and change `/ (root)` if it isn't already selected.
5. Click **Save**.

### Step 3: View Your Live Website!
GitHub will take about 30 seconds to build your site. Refresh the settings page, and you will see a banner at the top saying:
> 🔗 **Your site is live at:** `https://YOUR_GITHUB_USERNAME.github.io/parang-cnx/`

---

## 💻 Testing Locally

To check any edits locally before publishing them to the web:
1. Go to your workspace directory.
2. **Double-click `index.html`** in your file finder. It will open instantly in Safari, Chrome, or any other browser.
3. If you make a text change in your editor, save the file and click **Refresh (⌘R)** in your browser to see the update instantly!
