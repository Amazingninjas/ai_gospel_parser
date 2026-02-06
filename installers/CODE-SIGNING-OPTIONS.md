# Code Signing Certificate Options

Quick reference guide for purchasing a code signing certificate to eliminate Windows SmartScreen warnings.

## Recommended Providers (Ranked by Value)

### 1. Sectigo (Comodo) - BEST VALUE 💰
- **Price:** ~$120/year (Individual), ~$200/year (Organization)
- **Validation Time:** 2-3 business days
- **Reputation:** Good - trusted by Windows
- **URL:** https://sectigo.com/ssl-certificates-tls/code-signing
- **Best for:** Small developers, open-source projects, hobbyists

**Why choose:**
- Lowest cost from a reputable CA
- Fast validation process
- Good for individual developers
- Same trust level as more expensive options

### 2. SSL.com - GOOD BALANCE ⚖️
- **Price:** ~$180/year (Individual), ~$300/year (Organization)
- **Validation Time:** 2-4 business days
- **Reputation:** Good - growing recognition
- **URL:** https://www.ssl.com/certificates/code-signing/
- **Best for:** Professional developers, small businesses

**Why choose:**
- Competitive pricing
- Good customer support
- Multiple validation options
- Includes timestamping service

### 3. GlobalSign - PREMIUM ⭐
- **Price:** ~$200/year (Individual), ~$350/year (Organization)
- **Validation Time:** 3-5 business days
- **Reputation:** Excellent - well-established
- **URL:** https://www.globalsign.com/en/code-signing-certificate
- **Best for:** Established businesses, professional software

**Why choose:**
- Strong brand recognition
- Excellent support
- Good for building long-term reputation
- Enterprise options available

### 4. DigiCert - MOST TRUSTED 🏆
- **Price:** ~$400/year (Individual), ~$500/year (Organization)
- **Validation Time:** 1-2 business days (fastest)
- **Reputation:** Excellent - Microsoft's preferred CA
- **URL:** https://www.digecert.com/signing/code-signing-certificates
- **Best for:** Enterprise software, high-security needs, fastest validation

**Why choose:**
- Best reputation with Microsoft
- Fastest validation process
- Premium customer service
- Best for enterprise distribution

## Certificate Types

### Standard (OV/IV) Code Signing Certificate
- **Cost:** $120-400/year
- **Validation:** Organization (OV) or Individual (IV) validation
- **Storage:** USB token or software certificate (PFX file)
- **SmartScreen:** Builds reputation over time (weeks/months)
- **Best for:** Most developers

### Extended Validation (EV) Code Signing Certificate
- **Cost:** $300-700/year
- **Validation:** More rigorous identity verification
- **Storage:** Hardware token only (USB/YubiKey)
- **SmartScreen:** Immediate reputation (no warnings from day 1)
- **Best for:** Commercial software, immediate trust needed

**EV vs Standard:**
- EV eliminates SmartScreen warnings immediately
- Standard requires weeks/months to build reputation
- EV costs 2-3x more
- EV requires hardware token (cannot be copied/stolen)
- For small projects, Standard is usually sufficient

## What You'll Need

### For Individual Validation (IV):
- Government-issued photo ID (driver's license, passport)
- Phone number for verification callback
- Email address (domain-verified or personal)
- Business address (if applicable)

### For Organization Validation (OV):
- All of the above, plus:
- Business registration documents
- DUNS number or equivalent
- Proof of business address
- Authorized representative verification

### For Extended Validation (EV):
- All OV requirements, plus:
- More extensive business verification
- Physical address verification
- Operational existence verification

## Purchase Process

### Step 1: Choose Provider (15 minutes)
- Compare prices and features
- Check for discounts (first-year, bulk, open-source)
- Read reviews and reputation

### Step 2: Order Certificate (30 minutes)
- Select certificate type (Standard vs EV)
- Choose validation level (Individual vs Organization)
- Complete order form

### Step 3: Validation (2-5 business days)
- Submit required documents
- Respond to verification emails/calls
- Wait for approval

### Step 4: Download Certificate (15 minutes)
- Download PFX file (or receive hardware token for EV)
- Set strong password
- Store securely (backup!)

### Step 5: Sign Your Software (30 minutes)
- Install Windows SDK (for signtool.exe)
- Sign the .exe file
- Verify signature
- Test installer

## Signing Process

### Install Windows SDK:
```powershell
# Download from Microsoft
https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/

# Or via winget
winget install Microsoft.WindowsSDK
```

### Sign the .exe:
```cmd
# Navigate to installer directory
cd installers\windows\output

# Sign with timestamp
"C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe" sign ^
  /f "path\to\certificate.pfx" ^
  /p "certificate_password" ^
  /tr http://timestamp.digicert.com ^
  /td sha256 ^
  /fd sha256 ^
  AI-Gospel-Parser-Setup-1.0.1.exe

# Verify signature
signtool verify /pa /v AI-Gospel-Parser-Setup-1.0.1.exe
```

### Automate Signing (build-and-sign.bat):
```batch
@echo off
REM Build installer with Inno Setup
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

REM Sign the output
signtool sign /f "%CERT_PATH%" /p "%CERT_PASSWORD%" /tr http://timestamp.digicert.com /td sha256 /fd sha256 "output\AI-Gospel-Parser-Setup-1.0.1.exe"

REM Verify
signtool verify /pa /v "output\AI-Gospel-Parser-Setup-1.0.1.exe"
```

## Cost Analysis

### One-Time Costs:
- Certificate: $120-400
- Windows SDK: Free
- Hardware token (EV only): Included

### Annual Costs:
- Certificate renewal: $120-400/year
- No other costs

### Break-Even Analysis:
If distributing to:
- **10-50 users:** Documentation may be sufficient (see INSTALLATION-TROUBLESHOOTING.md)
- **50-200 users:** Standard certificate recommended
- **200+ users:** Standard or EV certificate highly recommended
- **Commercial software:** EV certificate recommended

### ROI Calculation:
- User time saved bypassing SmartScreen: ~5 minutes per user
- Support requests avoided: ~30% reduction
- Professional appearance: Priceless
- Break-even: ~50-100 users (at $150/year)

## Renewal

Certificates must be renewed annually:
- Renewal is faster than initial purchase (1-2 days)
- Keep same certificate to maintain SmartScreen reputation
- Price usually same as initial purchase
- Set calendar reminder 30 days before expiration

## Security Best Practices

### Protect Your Certificate:
- ✅ Use strong password (16+ characters, random)
- ✅ Store PFX file securely (encrypted drive)
- ✅ Backup to secure location
- ✅ Never share certificate or password
- ✅ Use separate certificate for each project (optional)

### After Signing:
- ✅ Test signed installer on clean Windows VM
- ✅ Verify no SmartScreen warnings (or reduced warnings)
- ✅ Delete unsigned versions
- ✅ Update download links

### If Certificate is Compromised:
- ⚠️ Revoke certificate immediately (contact CA)
- ⚠️ Purchase new certificate
- ⚠️ Re-sign all distributed software
- ⚠️ Notify users if necessary

## Discounts & Savings

### Open-Source Discounts:
Some CAs offer discounts for open-source projects:
- Sectigo: Case-by-case (contact sales)
- GlobalSign: Limited program (application required)
- DigiCert: No open-source program

### Multi-Year Purchase:
- 2-year: Usually 10-15% discount
- 3-year: Usually 20-25% discount
- But: Cannot transfer to different name/organization
- Consider if stable long-term project

### Student/Education Discounts:
Some CAs offer education pricing:
- Check if your .edu email qualifies
- Usually 30-50% discount
- Verify eligibility before purchase

## Alternatives to Code Signing

If certificate cost is prohibitive:

### 1. Microsoft Store Distribution:
- **Cost:** $19 one-time developer account
- **Pros:** Automatic trust, built-in updates, professional
- **Cons:** Strict requirements, review process, revenue share

### 2. Improved Documentation:
- Clear bypass instructions (already created)
- Video tutorials showing installation
- Build reputation through downloads over time

### 3. ZIP Distribution:
- Package installer as .zip file
- Slightly less suspicious to Windows
- Users extract, then run .exe
- Still shows warnings but different UX

### 4. PowerShell/Script Installer:
- Less likely to trigger SmartScreen
- Can download and setup application
- Requires ExecutionPolicy bypass
- More technical user experience

## Recommendation

**For AI Gospel Parser:**

**Immediate (Current):**
- ✅ Use documentation approach (INSTALLATION-TROUBLESHOOTING.md)
- ✅ Provide checksums for verification
- ✅ Build reputation through GitHub releases

**Short-term (if 50+ users):**
- Consider **Sectigo Individual Certificate** ($120/year)
- Best value for money
- Sufficient for open-source project
- Build SmartScreen reputation over 2-3 months

**Long-term (if 200+ users or commercial):**
- Consider **EV Certificate** ($300-500/year)
- Immediate trust, no warnings
- Professional appearance
- Worth the investment for serious distribution

## Next Steps

1. **Track download numbers** - Wait to see user adoption
2. **Monitor feedback** - See if SmartScreen causes issues
3. **Decide threshold** - If 50+ users or high support burden, get certificate
4. **Budget accordingly** - Plan $150-200 annual cost
5. **Purchase when ready** - Follow this guide for provider selection

## Questions?

- Check INSTALLATION-TROUBLESHOOTING.md for user guidance
- See SMARTSCREEN-ISSUE.md for technical details
- Research providers based on your needs and budget
- Contact sales representatives for quotes and questions

Remember: Documentation is free and works for small projects. Code signing is an investment that makes sense at scale.
