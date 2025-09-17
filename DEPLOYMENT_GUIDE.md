# Axora Website Deployment Guide

## 🚀 **Quick Deploy to GitHub Pages (Recommended)**

### **Step 1: Create GitHub Repository**

1. Go to [GitHub.com](https://github.com)
2. Click "New repository"
3. Name it `axora` or `axora-website`
4. Make it **Public** (required for free GitHub Pages)
5. Click "Create repository"

### **Step 2: Upload Your Code**

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial Axora website"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/axora.git

# Push to GitHub
git push -u origin main
```

### **Step 3: Enable GitHub Pages**

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll down to **Pages** section
4. Under **Source**, select **GitHub Actions**
5. Your site will be available at: `https://YOUR_USERNAME.github.io/axora`

## 🌐 **Custom Domain Setup (Optional)**

### **Option 1: Buy a Domain**

1. **Recommended**: [Namecheap](https://namecheap.com) - `axora.com` (~$10/year)
2. **Alternative**: [GoDaddy](https://godaddy.com) - `axora.com` (~$12/year)
3. **Budget**: [Freenom](https://freenom.com) - `axora.tk` (FREE!)

### **Option 2: Configure Custom Domain**

1. In your GitHub repository, go to **Settings** → **Pages**
2. Under **Custom domain**, enter your domain (e.g., `axora.com`)
3. Add a `CNAME` file to your repository:
   ```
   axora.com
   ```
4. Configure DNS with your domain provider:
   - **Type**: CNAME
   - **Name**: www
   - **Value**: YOUR_USERNAME.github.io

## 🎯 **Alternative Hosting Options**

### **Netlify (Drag & Drop)**

1. Go to [Netlify.com](https://netlify.com)
2. Drag your `downloads` folder to the deploy area
3. Get instant URL: `https://random-name.netlify.app`
4. **Custom domain**: Add in Netlify dashboard

### **Vercel (GitHub Integration)**

1. Go to [Vercel.com](https://vercel.com)
2. Connect your GitHub account
3. Import your repository
4. Deploy automatically
5. Get URL: `https://axora.vercel.app`

### **Firebase Hosting**

1. Install Firebase CLI: `npm install -g firebase-tools`
2. Run: `firebase init hosting`
3. Run: `firebase deploy`
4. Get URL: `https://axora.web.app`

## 📊 **Comparison Table**

| Platform         | Free Domain | Custom Domain | Ease       | Speed      | Features         |
| ---------------- | ----------- | ------------- | ---------- | ---------- | ---------------- |
| **GitHub Pages** | ✅          | ✅            | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | CI/CD, HTTPS     |
| **Netlify**      | ✅          | ✅            | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Forms, Functions |
| **Vercel**       | ✅          | ✅            | ⭐⭐⭐⭐   | ⭐⭐⭐⭐⭐ | Serverless       |
| **Firebase**     | ✅          | ✅            | ⭐⭐⭐     | ⭐⭐⭐⭐   | Google Cloud     |

## 🎯 **My Recommendation**

**For Axora**: Use **GitHub Pages** + **Custom Domain**

**Why?**

- ✅ Completely free
- ✅ Professional subdomain: `yourusername.github.io/axora`
- ✅ Easy custom domain: `axora.com`
- ✅ Automatic HTTPS
- ✅ Fast global CDN
- ✅ Already configured with GitHub Actions
- ✅ Version control for your website

## 🚀 **Next Steps**

1. **Create GitHub repository** (5 minutes)
2. **Upload your code** (2 minutes)
3. **Enable GitHub Pages** (1 minute)
4. **Optional**: Buy `axora.com` domain (~$10/year)
5. **Optional**: Configure custom domain (5 minutes)

**Total time**: 10-15 minutes for a professional website!

---

**Need help?** Contact Aditya Kuchhal for deployment assistance.

