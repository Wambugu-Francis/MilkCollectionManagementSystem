import os
from pathlib import Path

# Get the current directory
BASE_DIR = Path(__file__).resolve().parent

print("🔧 Creating Template Files...")
print(f"📁 Project Directory: {BASE_DIR}")

# Create templates directory structure
templates_dir = BASE_DIR / 'broker' / 'templates' / 'broker'
templates_dir.mkdir(parents=True, exist_ok=True)
print(f"✅ Created directory: {templates_dir}")

# Template files and their content
templates = {
    'base.html': '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Milk Broker System{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="nav-brand">
                <h1>🥛 Milk Broker System</h1>
            </div>
            <ul class="nav-menu">
                <li><a href="{% url 'dashboard' %}" class="nav-link">Dashboard</a></li>
                <li><a href="{% url 'farmer_list' %}" class="nav-link">Farmers</a></li>
                <li><a href="{% url 'collection_create' %}" class="nav-link">Record Collection</a></li>
                <li><a href="{% url 'collection_history' %}" class="nav-link">History</a></li>
                <li><a href="/admin/" class="nav-link">Admin</a></li>
            </ul>
        </div>
    </nav>

    <main class="main-content">
        <div class="container">
            {% if messages %}
                <div class="messages">
                    {% for message in messages %}
                        <div class="alert alert-{{ message.tags }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}

            {% block content %}{% endblock %}
        </div>
    </main>

    <footer class="footer">
        <div class="container">
            <p>&copy; 2024 Milk Broker Management System. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>''',

    'dashboard.html': '''{% extends 'broker/base.html' %}
{% block title %}Dashboard - Milk Broker System{% endblock %}

{% block content %}
<div class="dashboard">
    <h2 class="page-title">Dashboard Overview</h2>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-icon">👨‍🌾</div>
            <div class="stat-info">
                <h3>Total Farmers</h3>
                <p class="stat-number">{{ total_farmers }}</p>
            </div>
        </div>

        <div class="stat-card">
            <div class="stat-icon">🥛</div>
            <div class="stat-info">
                <h3>Today's Collection</h3>
                <p class="stat-number">{{ today_quantity|floatformat:2 }}L</p>
            </div>
        </div>

        <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-info">
                <h3>Today's Revenue</h3>
                <p class="stat-number">KES {{ today_revenue|floatformat:2 }}</p>
            </div>
        </div>

        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-info">
                <h3>Monthly Collection</h3>
                <p class="stat-number">{{ month_quantity|floatformat:2 }}L</p>
            </div>
        </div>
    </div>

    <div class="dashboard-grid">
        <div class="dashboard-section">
            <h3>Recent Collections</h3>
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Farmer</th>
                            <th>Quantity (L)</th>
                            <th>Date</th>
                            <th>Amount</th>
                            <th>SMS</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for collection in recent_collections %}
                        <tr>
                            <td>{{ collection.farmer.farmer_id }}</td>
                            <td>{{ collection.quantity }}</td>
                            <td>{{ collection.collection_date }}</td>
                            <td>KES {{ collection.total_amount }}</td>
                            <td>
                                {% if collection.sms_sent %}
                                    <span class="badge badge-success">✓ Sent</span>
                                {% else %}
                                    <span class="badge badge-warning">✗ Failed</span>
                                {% endif %}
                            </td>
                        </tr>
                        {% empty %}
                        <tr>
                            <td colspan="5" class="text-center">No collections yet</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <div class="dashboard-section">
            <h3>Top Farmers (All Time)</h3>
            <div class="farmers-list">
                {% for farmer in top_farmers %}
                <div class="farmer-item">
                    <div class="farmer-info">
                        <strong>{{ farmer.farmer_id }}</strong>
                        <span>{{ farmer.first_name }} {{ farmer.last_name }}</span>
                    </div>
                    <div class="farmer-stat">
                        {{ farmer.total_milk|floatformat:2 }}L
                    </div>
                </div>
                {% empty %}
                <p class="text-muted">No farmers yet</p>
                {% endfor %}
            </div>
        </div>
    </div>

    <div class="quick-actions">
        <a href="{% url 'farmer_create' %}" class="btn btn-primary">Register New Farmer</a>
        <a href="{% url 'collection_create' %}" class="btn btn-success">Record Collection</a>
        <a href="{% url 'farmer_list' %}" class="btn btn-secondary">View All Farmers</a>
    </div>
</div>
{% endblock %}''',

    'farmer_list.html': '''{% extends 'broker/base.html' %}
{% block title %}Farmers List{% endblock %}

{% block content %}
<div class="page-header">
    <h2 class="page-title">Registered Farmers</h2>
    <a href="{% url 'farmer_create' %}" class="btn btn-primary">+ Register New Farmer</a>
</div>

<div class="search-box">
    <form method="get" action="{% url 'farmer_list' %}">
        <input type="text" name="q" placeholder="Search by name, ID, phone, location..." 
               value="{{ query }}" class="search-input">
        <button type="submit" class="btn btn-search">Search</button>
    </form>
</div>

<div class="table-container">
    <table class="data-table">
        <thead>
            <tr>
                <th>Farmer ID</th>
                <th>Name</th>
                <th>Phone Number</th>
                <th>Location</th>
                <th>Registered</th>
                <th>Status</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for farmer in farmers %}
            <tr>
                <td><strong>{{ farmer.farmer_id }}</strong></td>
                <td>{{ farmer.first_name }} {{ farmer.last_name }}</td>
                <td>{{ farmer.phone_number }}</td>
                <td>{{ farmer.location }}</td>
                <td>{{ farmer.date_registered|date:"M d, Y" }}</td>
                <td>
                    {% if farmer.is_active %}
                        <span class="badge badge-success">Active</span>
                    {% else %}
                        <span class="badge badge-danger">Inactive</span>
                    {% endif %}
                </td>
                <td>
                    <a href="{% url 'farmer_detail' farmer.pk %}" class="btn-small btn-info">View</a>
                    <a href="{% url 'farmer_update' farmer.pk %}" class="btn-small btn-warning">Edit</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="7" class="text-center">No farmers found</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',

    'farmer_detail.html': '''{% extends 'broker/base.html' %}
{% block title %}{{ farmer.first_name }} {{ farmer.last_name }} - Details{% endblock %}

{% block content %}
<div class="page-header">
    <h2 class="page-title">Farmer Details</h2>
    <div class="btn-group">
        <a href="{% url 'farmer_update' farmer.pk %}" class="btn btn-warning">Edit Details</a>
        <a href="{% url 'farmer_list' %}" class="btn btn-secondary">Back to List</a>
    </div>
</div>

<div class="detail-grid">
    <div class="detail-card">
        <h3>Personal Information</h3>
        <div class="detail-row">
            <span class="detail-label">Farmer ID:</span>
            <span class="detail-value"><strong>{{ farmer.farmer_id }}</strong></span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Full Name:</span>
            <span class="detail-value">{{ farmer.first_name }} {{ farmer.last_name }}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Phone Number:</span>
            <span class="detail-value">{{ farmer.phone_number }}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">ID Number:</span>
            <span class="detail-value">{{ farmer.id_number }}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Location:</span>
            <span class="detail-value">{{ farmer.location }}</span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Status:</span>
            <span class="detail-value">
                {% if farmer.is_active %}
                    <span class="badge badge-success">Active</span>
                {% else %}
                    <span class="badge badge-danger">Inactive</span>
                {% endif %}
            </span>
        </div>
        <div class="detail-row">
            <span class="detail-label">Registered:</span>
            <span class="detail-value">{{ farmer.date_registered|date:"F d, Y" }}</span>
        </div>
        {% if farmer.notes %}
        <div class="detail-row">
            <span class="detail-label">Notes:</span>
            <span class="detail-value">{{ farmer.notes }}</span>
        </div>
        {% endif %}
    </div>

    <div class="detail-card">
        <h3>Collection Statistics</h3>
        <div class="stats-small">
            <div class="stat-small-item">
                <p class="stat-small-label">Total Collected</p>
                <p class="stat-small-value">{{ total_collected|floatformat:2 }}L</p>
            </div>
            <div class="stat-small-item">
                <p class="stat-small-label">This Month</p>
                <p class="stat-small-value">{{ month_collected|floatformat:2 }}L</p>
            </div>
            <div class="stat-small-item">
                <p class="stat-small-label">Total Revenue</p>
                <p class="stat-small-value">KES {{ total_revenue|floatformat:2 }}</p>
            </div>
        </div>
    </div>
</div>

<div class="collections-section">
    <h3>Recent Collections</h3>
    <div class="table-container">
        <table class="data-table">
            <thead>
                <tr>
                    <th>Date</th>
                    <th>Quantity (L)</th>
                    <th>Price/L</th>
                    <th>Total Amount</th>
                    <th>SMS Status</th>
                </tr>
            </thead>
            <tbody>
                {% for collection in collections %}
                <tr>
                    <td>{{ collection.collection_date }}</td>
                    <td>{{ collection.quantity }}</td>
                    <td>KES {{ collection.price_per_liter }}</td>
                    <td>KES {{ collection.total_amount }}</td>
                    <td>
                        {% if collection.sms_sent %}
                            <span class="badge badge-success">Sent</span>
                        {% else %}
                            <span class="badge badge-warning">Failed</span>
                        {% endif %}
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="5" class="text-center">No collections yet</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}''',

    'farmer_form.html': '''{% extends 'broker/base.html' %}
{% block title %}{{ title }}{% endblock %}

{% block content %}
<div class="page-header">
    <h2 class="page-title">{{ title }}</h2>
    <a href="{% url 'farmer_list' %}" class="btn btn-secondary">Cancel</a>
</div>

<div class="form-container">
    <form method="post" class="form">
        {% csrf_token %}

        <div class="form-row">
            <div class="form-group">
                <label for="{{ form.first_name.id_for_label }}">First Name *</label>
                {{ form.first_name }}
                {% if form.first_name.errors %}
                    <span class="error">{{ form.first_name.errors.0 }}</span>
                {% endif %}
            </div>

            <div class="form-group">
                <label for="{{ form.last_name.id_for_label }}">Last Name *</label>
                {{ form.last_name }}
                {% if form.last_name.errors %}
                    <span class="error">{{ form.last_name.errors.0 }}</span>
                {% endif %}
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="{{ form.phone_number.id_for_label }}">Phone Number *</label>
                {{ form.phone_number }}
                <small class="form-help">Format: +254712345678 or 0712345678</small>
                {% if form.phone_number.errors %}
                    <span class="error">{{ form.phone_number.errors.0 }}</span>
                {% endif %}
            </div>

            <div class="form-group">
                <label for="{{ form.id_number.id_for_label }}">ID Number *</label>
                {{ form.id_number }}
                {% if form.id_number.errors %}
                    <span class="error">{{ form.id_number.errors.0 }}</span>
                {% endif %}
            </div>
        </div>

        <div class="form-group">
            <label for="{{ form.location.id_for_label }}">Location *</label>
            {{ form.location }}
            {% if form.location.errors %}
                <span class="error">{{ form.location.errors.0 }}</span>
            {% endif %}
        </div>

        <div class="form-group">
            <label for="{{ form.notes.id_for_label }}">Additional Notes</label>
            {{ form.notes }}
            {% if form.notes.errors %}
                <span class="error">{{ form.notes.errors.0 }}</span>
            {% endif %}
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Save Farmer</button>
            <a href="{% url 'farmer_list' %}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}''',

    'collection_form.html': '''{% extends 'broker/base.html' %}
{% block title %}Record Milk Collection{% endblock %}

{% block content %}
<div class="page-header">
    <h2 class="page-title">Record Milk Collection</h2>
    <a href="{% url 'dashboard' %}" class="btn btn-secondary">Cancel</a>
</div>

<div class="form-container">
    <form method="post" class="form">
        {% csrf_token %}

        <div class="form-group">
            <label for="{{ form.farmer.id_for_label }}">Select Farmer *</label>
            {{ form.farmer }}
            {% if form.farmer.errors %}
                <span class="error">{{ form.farmer.errors.0 }}</span>
            {% endif %}
        </div>

        <div class="form-row">
            <div class="form-group">
                <label for="{{ form.quantity.id_for_label }}">Quantity (Liters) *</label>
                {{ form.quantity }}
                {% if form.quantity.errors %}
                    <span class="error">{{ form.quantity.errors.0 }}</span>
                {% endif %}
            </div>

            <div class="form-group">
                <label for="{{ form.price_per_liter.id_for_label }}">Price per Liter *</label>
                {{ form.price_per_liter }}
                {% if form.price_per_liter.errors %}
                    <span class="error">{{ form.price_per_liter.errors.0 }}</span>
                {% endif %}
            </div>
        </div>

        <div class="form-group">
            <label for="{{ form.collection_date.id_for_label }}">Collection Date *</label>
            {{ form.collection_date }}
            {% if form.collection_date.errors %}
                <span class="error">{{ form.collection_date.errors.0 }}</span>
            {% endif %}
        </div>

        <div class="form-group">
            <label for="{{ form.notes.id_for_label }}">Notes</label>
            {{ form.notes }}
            {% if form.notes.errors %}
                <span class="error">{{ form.notes.errors.0 }}</span>
            {% endif %}
        </div>

        <div class="alert alert-info">
            📱 An SMS will be automatically sent to the farmer after recording this collection.
        </div>

        <div class="form-actions">
            <button type="submit" class="btn btn-success">Record Collection & Send SMS</button>
            <a href="{% url 'dashboard' %}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}''',

    'collection_history.html': '''{% extends 'broker/base.html' %}
{% block title %}Collection History{% endblock %}

{% block content %}
<div class="page-header">
    <h2 class="page-title">Collection History</h2>
    <a href="{% url 'collection_create' %}" class="btn btn-primary">+ Record New Collection</a>
</div>

<div class="filter-box">
    <form method="get" class="filter-form">
        <div class="filter-group">
            <label>Farmer:</label>
            <select name="farmer" class="form-input">
                <option value="">All Farmers</option>
                {% for farmer in farmers %}
                    <option value="{{ farmer.id }}">{{ farmer.farmer_id }} - {{ farmer.first_name }} {{ farmer.last_name }}</option>
                {% endfor %}
            </select>
        </div>
        <div class="filter-group">
            <label>From:</label>
            <input type="date" name="date_from" class="form-input">
        </div>
        <div class="filter-group">
            <label>To:</label>
            <input type="date" name="date_to" class="form-input">
        </div>
        <button type="submit" class="btn btn-search">Filter</button>
    </form>
</div>

<div class="stats-summary">
    <div class="summary-item">
        <strong>Total Quantity:</strong> {{ total_quantity|floatformat:2 }}L
    </div>
    <div class="summary-item">
        <strong>Total Revenue:</strong> KES {{ total_revenue|floatformat:2 }}
    </div>
</div>

<div class="table-container">
    <table class="data-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Farmer ID</th>
                <th>Farmer Name</th>
                <th>Quantity (L)</th>
                <th>Price/L</th>
                <th>Total Amount</th>
                <th>SMS Status</th>
            </tr>
        </thead>
        <tbody>
            {% for collection in collections %}
            <tr>
                <td>{{ collection.collection_date }}</td>
                <td><strong>{{ collection.farmer.farmer_id }}</strong></td>
                <td>{{ collection.farmer.first_name }} {{ collection.farmer.last_name }}</td>
                <td>{{ collection.quantity }}</td>
                <td>KES {{ collection.price_per_liter }}</td>
                <td>KES {{ collection.total_amount }}</td>
                <td>
                    {% if collection.sms_sent %}
                        <span class="badge badge-success">✓ Sent</span>
                    {% else %}
                        <span class="badge badge-warning">✗ Failed</span>
                    {% endif %}
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="7" class="text-center">No collections found</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
{% endblock %}''',
}

# Create each template file
for filename, content in templates.items():
    filepath = templates_dir / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Created: {filepath}")

print("\n✨ Done! All template files created successfully!")
print(f"\n📂 Templates location: {templates_dir}")
print("\n📄 Files created:")
for filename in templates.keys():
    print(f"   ✓ {filename}")

print("\n🚀 You can now run: python manage.py runserver")
print("   Templates should load correctly!")