# 🧙 Monsteriada PrestaShop Clone Project

**PrestaShop website clone for the Electronic Business course**  
**Gdańsk University of Technology**

This project aims to recreate the core features and design of [monsteriada.pl](https://monsteriada.pl), using the PrestaShop platform. The project is part of the Electronic Business course curriculum, where we apply our knowledge in e-commerce development and project management.

## 👥 Team Information

**Team Name:**  
**404 - ErrorsNotFound**

**Team Members & Roles:**  
- **Igor Józefowicz** - Project Lead & Full Stack Developer 🧩
- **Anna Piszczewiat** - Backend Developer 🔧
- **Jan Rogowski** - Frontend Developer 🎨
- **Patryk Sowiński** - Testing & DevOps Engineer 🧪
- **Adam Zarzycki** - Data Engineer & Testing 🗃️

---

### **🛠️ Prestashop Core Development Team**
- **Anna Piszczewiat** - head of team
- **Igor Józefowicz**

### **🎨 Frontend & UI Team**
- **Jan Rogowski** - head of team
- **Igor Józefowicz**

### **🗃️ Data & Web Scraping Team**
- **Adam Zarzycki** - head of team
- **Patryk Sowiński**

### **🧪 Testing Team**
- **Patryk Sowiński** - head of team
- **Adam Zarzycki**

### **🚀 Deployment & Integration Team**
- **Igor Józefowicz** - head of team
- **Patryk Sowiński**

---

## 📋 Project Details

- **Cloning Site:** [monsteriada.pl](https://monsteriada.pl) - a Polish e-commerce site specializing in fantasy & science fiction related products
- **Software Version:** PrestaShop 1.7.8.11
- **Repository Language:** English
- **Project Requirements:**  
  The repository contains a README.md file with:
  - 📄 A project description
  - ⚙️ Software version information
  - 🚀 Startup/installation instructions
  - 👥 Team composition

## 🛠️ Project Installation Guidelines

- **Project directory:** `/src/monsteriada-prestashop-clone`
- **Database name:** `monsteriada`
- **Database dev user:** `root`
- **Database dev password:** `root`
- **Admin panel directory:** `/admin-dev`

**Fixing permissions after cloning the project:**\
`sudo chmod -R 777 ./src`

**The database is automatically initialized from the `/data/db.sql`**

**To manually import database:**\
`docker exec -i mariadb mysql -u root -proot monsteriada < ./data/db.sql`

**To manually export database:**\
`docker exec mariadb mysqldump --user=root -proot monsteriada > ./data/db.sql`

---
