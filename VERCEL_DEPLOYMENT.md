# Axora Vercel Deployment Guide

## 🚀 **Quick Deploy to Vercel**

### **Step 1: Prepare Your Code**

```bash
# Build for Vercel
python3 build_vercel.py
```

### **Step 2: Deploy to Vercel**

#### **Option A: GitHub Integration (Recommended)**

1. **Push to GitHub**:

   ```bash
   git add .
   git commit -m "Add Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel**:

   - Go to [vercel.com](https://vercel.com)
   - Sign up/Login with GitHub
   - Click **"New Project"**
   - Import your GitHub repository
   - Click **"Deploy"**

3. **Your site will be live at**: `https://axora.vercel.app`

#### **Option B: Vercel CLI (Advanced)**

1. **Install Vercel CLI**:

   ```bash
   npm install -g vercel
   ```

2. **Deploy**:

   ```bash
   vercel
   ```

3. **Follow the prompts** and your site will be live!

## 🌐 **Custom Domain Setup**

### **Step 1: Add Custom Domain**

1. Go to your Vercel dashboard
2. Select your Axora project
3. Go to **Settings** → **Domains**
4. Add your domain: `axora.com`

### **Step 2: Configure DNS**

Add these DNS records with your domain provider:

**For Root Domain (axora.com):**

- **Type**: A
- **Name**: @
- **Value**: 76.76.19.61

**For WWW (www.axora.com):**

- **Type**: CNAME
- **Name**: www
- **Value**: cname.vercel-dns.com

### **Step 3: SSL Certificate**

- Vercel automatically provides SSL certificates
- Your site will be available at `https://axora.com`

## 📊 **Vercel Features for Axora**

### **✅ What You Get:**

- **Free Tier**: Unlimited bandwidth
- **Global CDN**: Fast loading worldwide
- **Automatic HTTPS**: Secure connections
- **Custom Domains**: Professional URLs
- **Git Integration**: Auto-deploy on push
- **Preview Deployments**: Test before going live
- **Analytics**: Track visitors and performance

### **📈 Performance:**

- **Speed**: ⭐⭐⭐⭐⭐ (Global CDN)
- **Uptime**: 99.99% SLA
- **Security**: Automatic HTTPS, DDoS protection
- **Scalability**: Handles traffic spikes automatically

## 🔧 **Configuration Files**

### **vercel.json** (Already created)

```json
{
  "version": 2,
  "name": "axora",
  "builds": [
    {
      "src": "public/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/public/$1"
    }
  ]
}
```

### **build_vercel.py** (Already created)

- Builds macOS app
- Creates Windows placeholder
- Prepares files for Vercel
- Creates download zips

## 🎯 **Deployment Workflow**

### **Automatic Deployment:**

1. **Push to GitHub** → **Vercel auto-deploys**
2. **Preview URL**: `https://axora-git-main.vercel.app`
3. **Production URL**: `https://axora.vercel.app`

### **Manual Deployment:**

1. **Run**: `python3 build_vercel.py`
2. **Upload**: `public/` folder to Vercel
3. **Deploy**: Click deploy button

## 🚀 **Next Steps**

1. **Run the build script**: `python3 build_vercel.py`
2. **Push to GitHub**: `git push origin main`
3. **Deploy on Vercel**: Import repository
4. **Add custom domain**: `axora.com` (optional)
5. **Share your site**: `https://axora.vercel.app`

## 📞 **Need Help?**

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Support**: Contact Aditya Kuchhal
- **Issues**: Check GitHub repository

---

**Built with ❤️ by Aditya Kuchhal**

