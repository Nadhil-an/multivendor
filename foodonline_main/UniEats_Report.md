# Project Report: UniEats  
**Web-Based Campus Food Pre-Ordering Platform**

---

## 1. Title Page
**Project Title**: UniEats (Formerly CampusBite)  
**Institution**: Lovely Professional University  
**Degree**: Bachelor of Computer Applications (BCA)  
**Session**: 2025–2026

**Submitted By**:
- Adhithyan V.V. (12322517)
- Bommanaboina Srinivasulu (12320599)
- Abhinav T.S. (12306552)
- Michael Gatsi (12302727)
- Nadil (12303534)

**Supervised By**:  
Dr. Shilpi Singh  
Lovely Faculty of Computer Science, LPU

---

## 2. Introduction
With the rapid development of digital technologies, everyday services are transitioning from manual processes to efficient online systems. **UniEats** is a specialized web-based pre-ordering platform designed to solve the significant problem of overcrowding and long waiting times at University food courts.

Traditional manual ordering leads to wasted time for students and inefficient management for vendors. UniEats bridges this gap by providing an end-to-end digital solution for ordering, payment, and pickup.

---

## 3. Technology Stack
The platform is built using modern, production-grade technologies:
- **Backend Framework**: Python 3.x with **Django 5.2**.
- **Database**: **PostgreSQL** (Production) / SQLite (Development).
- **Frontend**: HTML5, CSS3 (Vanilla), and JavaScript.
- **Payment Integration**: **Razorpay API** for secure, automated transactions.
- **Mailing System**: SMTP integration for automated order confirmations and vendor approval alerts.
- **API Support**: Django REST Framework (DRF) for potential future mobile application scaling.

---

## 4. Problem Statement & Scope
### Problem Statement
Students frequently face long queues during peak hours (lunch breaks), leading to time wastage. Vendors struggle to manage high volumes of simultaneous orders manually, often resulting in order errors and congestion.

### Scope
- **Vendor Management**: Stalls can manage menus, categories, and opening hours.
- **Customer Pre-ordering**: Students browse, cart, and pay for food before arrival.
- **Secure Payments**: Integration of payment gateways to eliminate cash handling at stalls.
- **Order Tracking**: Unique token-based pickup system to ensure order accuracy.

---

## 5. System Analysis & Modules
### 5.1 User Modules
1. **Administrator**: Global monitoring, user activation/deactivation, and vendor approval management.
2. **Vendor (Restaurant Owner)**: Dashboard for menu updates, opening hour scheduling, and order fulfillment.
3. **Student (Customer)**: Search functionality, persistent shopping cart, and personal order history.

### 5.2 Key Technical Features
- **Slugified URLs**: Clean, SEO-friendly endpoints for all vendors and menu items.
- **Email Triggers**: Automated emails for account activation and order receipts.
- **Persistent Cart**: Items remain in the student's cart even after refreshing or logging out.
- **Tax & Fee Calculation**: Automated tax logic stored in JSON format within orders for transparency.

---

## 6. Database Design (ER Details)
The UniEats system uses a complex relational schema:
1.  **User**: Core authentication (Extends `AbstractBaseUser`).
2.  **UserProfile**: Extended metadata (Address, Phone, Location).
3.  **Vendor**: Links Users to Stall management.
4.  **OpeningHour**: Day-wise scheduling for vendors.
5.  **Category**: Grouping for menu items (e.g., "Main Course", "Beverages").
6.  **FoodItem**: Specific dishes with pricing, availability, and images.
7.  **Cart**: Real-time storage of student selections.
8.  **Tax**: Global and category-specific tax configuration.
9.  **Payment**: Logging of transaction IDs and status from Razorpay.
10. **Order**: Grand-total tracking and ownership.
11. **OrderedFood**: Snapshot of food items at the time of purchase.

---

## 7. Security Measures
1. **Data Sanitization**: Use of Django's ORM to prevent SQL Injection.
2. **CSRF Protection**: Cross-Site Request Forgery tokens on all forms.
3. **Password Hashing**: Industry-standard PBKDF2 hashing via Django auth.
4. **Honeypot Integration**: `django-admin-honeypot` to detect and block unauthorized admin login attempts.
5. **Secure Payment**: Processing all sensitive payment data through Razorpay’s secure infrastructure.

---

## 8. Requirements
### Hardware
- Processor: Intel i3 or above.
- RAM: 4GB Minimum.
- Storage: 100MB for application files.

### Software
- OS: Windows 10/11 or Linux.
- Python 3.10+
- Django 5.x
- Browser: Chrome, Firefox, or Edge.

---

## 9. Conclusion & Future Scope
UniEats provides a comprehensive solution for campus food management. It improves the student experience by saving time and helps vendors optimize their business operations.

**Future Scope**:
- **Mobile Application**: Native Android/iOS apps using the existing REST API.
- **QR Code Pickup**: Scanning tokens at stalls for even faster verification.
- **AI Recommendations**: Suggesting food items based on past student behavior.
- **Real-time Order Status**: Using WebSockets for live "Order Ready" notifications.
