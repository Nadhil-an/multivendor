def detectUser(user):
    if user.role == 1:   # Vendor
        return 'vendorDashboard'
    elif user.role == 2:  # Customer
        return 'customerDashboard'
    elif user.is_superuser:   # ✅ Django's built-in superuser check
        return '/admin'
    else:
        return 'home'
