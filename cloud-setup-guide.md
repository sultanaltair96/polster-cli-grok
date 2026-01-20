# 🚀 Polster CLI: Azure Data Lake Storage Setup Guide

**Transform your data factory from local to cloud-scale!** ☁️

This comprehensive guide walks you through setting up Azure Data Lake Storage (ADLS) with Polster CLI, giving your data pipelines unlimited scalability and durability.

---

## 📋 Table of Contents

- [🎯 Why Use Cloud Storage?](#-why-use-cloud-storage)
- [📋 Prerequisites](#-prerequisites)
- [⚡ Quick Start (15 minutes)](#-quick-start-15-minutes)
- [🔧 Step-by-Step Azure Setup](#-step-by-step-azure-setup)
- [⚙️ Polster Configuration](#️-polster-configuration)
- [🧪 Testing & Verification](#-testing--verification)
- [🚀 Production Deployment](#-production-deployment)
- [💰 Cost Management](#-cost-management)
- [🔍 Troubleshooting](#-troubleshooting)
- [📈 Migration Guide](#-migration-guide)

---

## 🎯 Why Use Cloud Storage?

### **Local Storage Limitations**
- ❌ **Storage limits**: Tied to your computer's disk space
- ❌ **No collaboration**: Hard to share data with team members
- ❌ **Backup headaches**: Manual backups required
- ❌ **Scalability issues**: Struggles with large datasets

### **Cloud Storage Benefits**
- ✅ **Unlimited scale**: Petabytes of storage available
- ✅ **Team collaboration**: Everyone accesses the same data
- ✅ **Automatic backups**: Azure handles reliability
- ✅ **Global access**: Work from anywhere, anytime
- ✅ **Cost-effective**: Pay only for what you use

### **Polster's Cloud Integration**
Polster seamlessly integrates with Azure Data Lake Storage while maintaining automatic fallbacks to local storage if cloud is unavailable.

---

## 📋 Prerequisites

### **Azure Requirements**
- ✅ **Azure subscription** (free tier available)
- ✅ **Azure account** with resource creation permissions
- ✅ **Basic Azure knowledge** (or follow our step-by-step guide)

### **Polster Requirements**
- ✅ **Polster CLI installed** (`pip install polster`)
- ✅ **Project created** (`polster init my_project`)
- ✅ **Python virtual environment** activated

### **Optional Tools**
- 🟡 **Azure CLI** (for command-line setup)
- 🟡 **Azure Storage Explorer** (for browsing data)

---

## ⚡ Quick Start (15 minutes)

### **3-Step Cloud Setup**

```bash
# Step 1: Create Azure Storage Account
# (Use Azure Portal or CLI below)

# Step 2: Configure Polster
cd my_data_project
echo "STORAGE_BACKEND=adls" >> .env
echo "ADLS_ACCOUNT_NAME=your_account_name" >> .env
echo "ADLS_CONTAINER=polster-data" >> .env
echo "ADLS_ACCOUNT_KEY=your_key_here" >> .env

# Step 3: Test Connection
source .venv/bin/activate
python src/core/bronze_example.py
# Data now saves to Azure automatically!
```

### **What You'll Have**
- ✅ Cloud storage account ready
- ✅ Polster configured for cloud
- ✅ Automatic data synchronization
- ✅ Fallback to local if cloud fails

---

## 🔧 Step-by-Step Azure Setup

### **Option A: Azure Portal (Recommended for Beginners)**

#### **Step 1: Access Azure Portal**
1. Go to [https://portal.azure.com](https://portal.azure.com)
2. Sign in with your Azure account
3. Click **"Create a resource"** in the top-left

#### **Step 2: Create Storage Account**
1. Search for **"Storage account"**
2. Click **"Create"**
3. Fill in the basics:
   - **Subscription**: Choose your subscription
   - **Resource group**: Create new or select existing
   - **Storage account name**: Choose unique name (lowercase, numbers only)
   - **Region**: Select closest to you
   - **Performance**: Standard
   - **Redundancy**: Locally-redundant storage (LRS)

#### **Step 3: Enable Data Lake Storage**
1. Under **"Advanced"** tab
2. Check **"Enable hierarchical namespace"**
3. This enables Data Lake Storage Gen2 features

#### **Step 4: Configure Networking**
1. **Connectivity method**: Public endpoint (default)
2. **Network access**: Enabled from all networks (for now)
3. **Minimum TLS version**: 1.2

#### **Step 5: Create the Account**
1. Click **"Review + create"**
2. Review settings and click **"Create"**
3. Wait for deployment (usually 1-2 minutes)

#### **Step 6: Create Container**
1. Navigate to your new storage account
2. Click **"Containers"** in the left menu
3. Click **"+ Container"**
4. Name: `polster-data`
5. Public access level: Private
6. Click **"Create"**

#### **Step 7: Get Access Credentials**
1. In your storage account, click **"Access keys"** in left menu
2. Copy **"Key 1"** → **"Key value"**
3. Save this key securely (you'll need it for Polster)

### **Option B: Azure CLI (For Advanced Users)**

```bash
# Install Azure CLI if not installed
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login to Azure
az login

# Create resource group
az group create --name polster-resources --location eastus

# Create storage account with Data Lake enabled
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
  --resource-group polster-resources \
  --output table
```

---

## ⚙️ Polster Configuration

### **Create Environment Configuration**

Navigate to your Polster project and create a `.env` file:

```bash
cd my_data_project

# Create environment file
cat > .env << EOF
# Azure Data Lake Storage Configuration
STORAGE_BACKEND=adls
ADLS_ACCOUNT_NAME=youruniquesaccountname
ADLS_CONTAINER=polster-data
ADLS_BASE_PATH=polster/data
ADLS_ACCOUNT_KEY=your_access_key_here
EOF
```

### **Configuration Details**

| Variable | Description | Example |
|----------|-------------|---------|
| `STORAGE_BACKEND` | Storage type | `adls` (Azure) or `local` |
| `ADLS_ACCOUNT_NAME` | Your storage account name | `mystorageaccount123` |
| `ADLS_CONTAINER` | Container name | `polster-data` |
| `ADLS_BASE_PATH` | Folder path in container | `polster/data` |
| `ADLS_ACCOUNT_KEY` | Access key | `your_long_key_here` |

### **Security Best Practices**

🔒 **Never commit `.env` to version control!**
```bash
# Add to .gitignore
echo ".env" >> .gitignore
```

🔒 **Use managed identities in production**
```bash
# Instead of access keys, use Azure AD authentication
# Configure in Azure portal under "Identity"
```

🔒 **Regular key rotation**
- Rotate keys every 90 days
- Use Azure Key Vault for secret management

---

## 🧪 Testing & Verification

### **Test Cloud Connection**

```bash
# Activate virtual environment
source .venv/bin/activate

# Run bronze example (saves to cloud)
python src/core/bronze_example.py

# Check success message
# Should show: "bronze_orders_*.parquet saved to Azure"
```

### **Verify Data in Azure**

1. Go to [Azure Portal](https://portal.azure.com)
2. Navigate to your storage account
3. Click **"Containers"** → **"polster-data"**
4. You should see:
   ```
   polster/data/
   ├── bronze/
   │   └── bronze_orders_*.parquet
   ```

### **Test Full Pipeline**

```bash
# Run complete pipeline
python src/core/bronze_example.py
python src/core/silver_example.py
python src/core/gold_example.py

# Verify all layers in Azure
# Should see bronze/, silver/, gold/ folders
```

### **Test Dagster Orchestration**

```bash
# Launch Dagster
dagster dev

# In browser, materialize assets
# Verify data appears in Azure storage
```

### **Test Fallback Behavior**

```bash
# Temporarily remove ADLS credentials
mv .env .env.backup

# Run script (should use local storage)
python src/core/bronze_example.py

# Restore credentials
mv .env.backup .env
```

---

## 🚀 Production Deployment

### **Managed Identity Setup**

For enhanced security in production:

1. **Enable managed identity** on your Azure resources
2. **Grant appropriate permissions** to storage account
3. **Remove access keys** from configuration
4. **Update Polster config** to use managed identity

### **RBAC Permissions**

Set minimal required permissions:
- **Storage Blob Data Contributor** (for read/write)
- **Storage Account Contributor** (for management)

### **Monitoring & Logging**

```bash
# Enable Azure Monitor
az monitor diagnostic-settings create \
  --name polster-monitoring \
  --resource /subscriptions/.../storageAccounts/youraccount \
  --logs '[{"category": "StorageWrite", "enabled": true}]' \
  --metrics '[{"category": "Transaction", "enabled": true}]' \
  --workspace /subscriptions/.../workspaces/yourworkspace
```

### **Backup & Disaster Recovery**

- **Automatic replication**: Azure handles geo-redundancy
- **Point-in-time restore**: Available for ADLS Gen2
- **Cross-region replication**: For business continuity

---

## 💰 Cost Management

### **Azure Data Lake Storage Pricing**

| Service | Price | Free Tier |
|---------|--------|-----------|
| **Storage** | $0.018/GB/month | First 5GB free |
| **Operations** | $0.004/10,000 | First 100,000 free |
| **Data Transfer** | $0.01/GB outbound | N/A |

### **Cost Estimation Examples**

**Small Project** (10GB data, daily updates):
- Storage: $0.18/month
- Operations: ~$0.12/month
- **Total**: ~$0.30/month

**Medium Project** (100GB data, hourly updates):
- Storage: $1.80/month
- Operations: ~$1.20/month
- **Total**: ~$3.00/month

**Large Project** (1TB data, real-time updates):
- Storage: $18.00/month
- Operations: ~$12.00/month
- **Total**: ~$30.00/month

### **Cost Optimization Tips**

1. **Use appropriate storage tiers**
   - Hot: Frequently accessed data
   - Cool: Infrequently accessed (cheaper)
   - Archive: Long-term storage (cheapest)

2. **Implement lifecycle policies**
   ```bash
   # Auto-move old data to cheaper tiers
   az storage account management-policy create \
     --account-name youraccount \
     --policy @lifecycle-policy.json
   ```

3. **Monitor usage**
   - Azure Cost Management dashboard
   - Storage analytics and metrics

4. **Optimize data patterns**
   - Compress data before storage
   - Use columnar formats (Parquet)
   - Partition data efficiently

---

## 🔍 Troubleshooting

### **"ADLS connection fails"**

**Symptoms**: Scripts run but data stays local

**Solutions**:
```bash
# Check environment variables
cat .env

# Verify Azure account exists
az storage account show --name $ADLS_ACCOUNT_NAME

# Test network connectivity
curl -I https://$ADLS_ACCOUNT_NAME.dfs.core.windows.net

# Check credentials
az storage account keys list --account-name $ADLS_ACCOUNT_NAME
```

### **"Permission denied" errors**

**Solutions**:
- Verify access key is correct
- Check container exists and permissions
- Ensure ADLS_BASE_PATH is accessible
- Try with different container permissions

### **"Data not appearing in Azure"**

**Debug steps**:
1. Check Azure portal for error messages
2. Verify container name spelling
3. Confirm base path format
4. Test with Azure Storage Explorer

### **"Pipeline still uses local storage"**

**Check**:
- `.env` file exists in project root
- Variables spelled correctly (case-sensitive)
- No typos in account name/key
- Restarted Dagster after configuration

### **"Slow performance"**

**Optimizations**:
- Use larger batch sizes for uploads
- Compress data before storage
- Choose closer Azure regions
- Use Azure CDN for global distribution

### **Common Azure Issues**

**Firewall blocking access**:
- Temporarily disable firewall for testing
- Configure IP whitelisting in production

**Subscription limits**:
- Check Azure subscription quotas
- Request increases if needed

---

## 📈 Migration Guide

### **From Local to Cloud Storage**

#### **Phase 1: Setup (No Downtime)**
```bash
# Keep local storage as backup
# Set up Azure resources
# Configure Polster for cloud
# Test with sample data
```

#### **Phase 2: Gradual Migration**
```bash
# Update production environment
# Monitor for issues
# Keep local backup for rollback
```

#### **Phase 3: Full Migration**
```bash
# Verify all data migrated
# Remove local storage dependencies
# Update documentation
```

### **Data Migration Tools**

**Option 1: AzCopy (Microsoft tool)**
```bash
# Install AzCopy
# Copy local data to Azure
azcopy copy "/local/path/data/*" "https://account.dfs.core.windows.net/container/data" --recursive
```

**Option 2: Azure Data Factory**
- Create data pipelines for migration
- Schedule during low-traffic periods
- Monitor transfer progress

**Option 3: Polster Scripts**
```python
# Custom migration script
# Read from local, write to cloud
# Handle large datasets with chunking
```

### **Rollback Plan**

If issues occur:
1. **Immediate**: Switch back to local storage
2. **Short-term**: Fix Azure configuration
3. **Long-term**: Implement better monitoring

---

## 🎯 Success Checklist

- ✅ Azure storage account created
- ✅ Data Lake Gen2 enabled
- ✅ Container created
- ✅ Access credentials obtained
- ✅ Polster `.env` configured
- ✅ Test scripts run successfully
- ✅ Data appears in Azure portal
- ✅ Dagster orchestration works
- ✅ Fallback behavior verified
- ✅ Cost monitoring set up

---

## 🚀 Advanced Topics

### **Multi-Environment Setup**

```bash
# Development
STORAGE_BACKEND=local

# Staging
STORAGE_BACKEND=adls
ADLS_ACCOUNT_NAME=stagingaccount

# Production
STORAGE_BACKEND=adls
ADLS_ACCOUNT_NAME=productionaccount
```

### **Data Lake Organization**

```
/polster/data/
├── bronze/
│   ├── customers/
│   ├── orders/
│   └── inventory/
├── silver/
│   ├── customer_summary/
│   └── sales_analytics/
└── gold/
    ├── business_reports/
    └── executive_dashboards/
```

### **Integration with Other Tools**

**Power BI**: Direct connection to ADLS
**Azure Synapse**: Query data lake directly
**Databricks**: Mount ADLS as filesystem
**Azure Functions**: Event-driven processing

---

## 📞 Support & Community

### **Getting Help**
- **Polster Documentation**: Check this guide first
- **Azure Documentation**: Official Azure Data Lake docs
- **Community Forums**: Ask questions and share solutions
- **GitHub Issues**: Report bugs or request features

### **Best Practices**
- Always test with small datasets first
- Monitor costs regularly
- Implement proper backup strategies
- Use managed identities for security
- Keep credentials secure and rotated

---

**Congratulations!** 🎉 You've successfully set up cloud storage for your Polster data factory. Your pipelines now have unlimited scalability and enterprise-grade reliability.

**What's your first cloud-powered analysis going to be?** 🚀

---

*Built with ❤️ for data teams who want cloud-scale without the complexity.*

*Last updated: January 2026*