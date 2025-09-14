def detectUser(user):
    if user.role == 1:   # Vendor
        return 'vendorDashboard'
    elif user.role == 2:  # Customer
        return 'customerDashboard'
    else:
        return 'loginUser'
