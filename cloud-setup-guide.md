# 🚀 Polster CLI: Azure Data Lake Storage Setup

**Transform your data factory from local to cloud-scale in 15 minutes!** ☁️

This guide walks you through setting up Azure Data Lake Storage (ADLS) with Polster CLI for unlimited scalability and durability.

---

## 📋 Prerequisites

### **Azure Requirements**
- ✅ **Azure subscription** (free tier available at [portal.azure.com](https://portal.azure.com))
- ✅ **Azure account** with resource creation permissions

### **Polster Requirements**
- ✅ **Polster CLI installed** (`pip install polster`)
- ✅ **Project created** (`polster init my_project`)

---

## 🔧 Azure Setup (10 minutes)

### **Option A: Azure Portal (Recommended)**

#### **Step 1: Create Storage Account**
1. Go to [Azure Portal](https://portal.azure.com) → **"Create a resource"**
2. Search **"Storage account"** → **"Create"**
3. **Basics tab**:
   - **Subscription**: Choose your subscription
   - **Resource group**: Create new (e.g., `polster-resources`)
   - **Storage account name**: Unique name (lowercase, 3-24 chars)
   - **Region**: Select closest to you
   - **Performance**: Standard
   - **Redundancy**: Locally-redundant storage (LRS)

#### **Step 2: Enable Data Lake Storage**
1. **Advanced tab** → Check **"Enable hierarchical namespace"**
2. **Networking tab**: Keep defaults (public access)
3. **Review + create** → **"Create"**

#### **Step 3: Create Container**
1. Navigate to your storage account
2. **Containers** → **"+ Container"**
3. **Name**: `polster-data`
4. **Public access**: Private
5. **Create**

#### **Step 4: Get Access Key**
1. **Access keys** in left menu
2. Copy **"Key 1"** → **"Key value"**
3. **Save securely** - you'll need this for Polster!

### **Option B: Azure CLI**

```bash
# Login to Azure
az login

# Create storage account
az storage account create \
  --name youruniquesaccountname \
  --resource-group polster-resources \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2 \
  --enable-hierarchical-namespace true

# Create container
az storage container create \
  --account-name youruniquesaccountname \
  --name polster-data \
  --auth-mode key

# Get access key
az storage account keys list \
  --account-name youruniquesaccountname \
  --output table
```

---

## ⚙️ Polster Configuration (3 minutes)

### **Create Environment File**

```bash
cd my_data_project

# Create .env file
cat > .env << EOF
# Azure Data Lake Storage Configuration
STORAGE_BACKEND=adls
ADLS_ACCOUNT_NAME=youruniquesaccountname
ADLS_CONTAINER=polster-data
ADLS_BASE_PATH=polster/data
ADLS_ACCOUNT_KEY=your_access_key_here
EOF
```

### **Security Note**
🔒 **Never commit `.env` to version control!**
```bash
echo ".env" >> .gitignore
```

---

## 🧪 Test Connection (2 minutes)

### **Run Test Script**

```bash
# Activate virtual environment
source .venv/bin/activate

# Run bronze example (saves to cloud)
python src/core/bronze_example.py
```

### **Verify in Azure Portal**

1. Go to your storage account → **"Containers"** → **"polster-data"**
2. You should see: `polster/data/bronze/bronze_orders_*.parquet`

**Success!** 🎉 Your data factory now uses cloud storage.

---

## 💰 Cost Information

### **Free Tier Available**
- **First 5GB storage**: Free
- **100,000 operations**: Free
- **Perfect for getting started!**

### **Pricing (if you exceed free tier)**
- **Storage**: $0.018/GB/month
- **Operations**: $0.004/10,000 operations
- **Data transfer**: $0.01/GB outbound

**Example**: Small project (10GB) = ~$0.20/month

---

## 🔍 Quick Troubleshooting

### **Data not appearing in Azure?**
- Check `.env` file exists and variables are correct
- Verify account name and access key
- Ensure container name is `polster-data`

### **Permission errors?**
- Confirm access key is copied correctly
- Check Azure account has proper permissions
- Try regenerating access keys in Azure portal

### **Still using local storage?**
- Restart any running processes after creating `.env`
- Check for typos in environment variable names
- Ensure `.env` is in project root directory

---

## 🚀 What's Next?

**Your data factory is now cloud-powered!** ☁️

- **Run full pipeline**: `dagster dev` to orchestrate all layers
- **Scale unlimited**: Handle petabytes of data
- **Collaborate**: Share data with your team
- **Go production**: Use managed identities for security

**Questions?** Check the main README or create a GitHub issue.

**Happy data engineering!** 🚀

---

*Built with ❤️ for scaling data dreams to cloud reality.*