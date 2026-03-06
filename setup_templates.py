import os

base_dir = "D:/fundgrow"

files = {
"templates/base.html": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FundGrow - Crowdfunding Platform</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary sticky-top shadow">
        <div class="container">
            <a class="navbar-brand fw-bold fs-3" href="{{ url_for('main.index') }}"><i class="fas fa-seedling me-2"></i>FundGrow</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto fs-5">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('main.index') }}">Home</a>
                    </li>
                    {% if current_user.is_authenticated %}
                        {% if current_user.role == 'admin' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('admin.dashboard') }}">Dashboard</a></li>
                        {% elif current_user.role == 'startup' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('startup.dashboard') }}">Dashboard</a></li>
                        {% elif current_user.role == 'investor' %}
                            <li class="nav-item"><a class="nav-link" href="{{ url_for('investor.dashboard') }}">Dashboard</a></li>
                        {% endif %}
                        <li class="nav-item">
                            <span class="nav-link text-warning fw-bold"><i class="fas fa-user-circle me-1"></i>{{ current_user.name }}</span>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link text-danger" href="{{ url_for('auth.logout') }}">Logout</a>
                        </li>
                    {% else %}
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('auth.login') }}">Login</a></li>
                        <li class="nav-item"><a class="nav-link btn btn-warning text-dark fw-bold px-3 ms-2" href="{{ url_for('auth.register') }}">Register</a></li>
                    {% endif %}
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4 main-content">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }} alert-dismissible fade show shadow-sm" role="alert">
                        {{ message }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>

    <footer class="bg-dark text-white mt-5 py-4 text-center">
        <div class="container">
            <h5 class="fw-bold"><i class="fas fa-seedling text-success me-2"></i>FundGrow</h5>
            <p class="mb-0 text-muted">&copy; 2026 FundGrow. Empowering Startups & Investors.</p>
        </div>
    </footer>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
""",

"templates/index.html": """{% extends 'base.html' %}
{% block content %}
<div class="p-5 mb-5 bg-light rounded-3 shadow-sm text-center banner position-relative" style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);">
    <div class="container-fluid py-5 text-white position-relative z-index-1">
        <h1 class="display-3 fw-bold mb-3">Invest in the Future</h1>
        <p class="col-md-8 mx-auto fs-4 text-light">Join FundGrow. Connect with top-tier startup ideas and watch your investments flourish.</p>
        {% if not current_user.is_authenticated %}
        <a href="{{ url_for('auth.register') }}" class="btn btn-warning btn-lg fw-bold mt-3 shadow">Get Started Now</a>
        {% endif %}
    </div>
</div>

<div class="row mb-5 align-items-center bg-white p-4 rounded shadow-sm">
    <div class="col-md-6">
        <h2 class="fw-bold text-secondary mb-0"><i class="fas fa-rocket text-primary me-2"></i>Discover Projects</h2>
    </div>
    <div class="col-md-6 text-end">
        <form action="{{ url_for('main.index') }}" method="GET" class="d-inline-flex w-75">
            <span class="input-group-text bg-primary text-white border-primary"><i class="fas fa-filter"></i></span>
            <select name="category" class="form-select border-primary" onchange="this.form.submit()">
                <option value="">All Categories</option>
                {% for c in categories %}
                    <option value="{{ c }}" {% if selected_category == c %}selected{% endif %}>{{ c }}</option>
                {% endfor %}
            </select>
        </form>
    </div>
</div>

<div class="row">
    {% for project in projects %}
        {% set percent = (project.raised_amount / project.goal_amount * 100)|round(2) %}
        {% if percent > 100 %}{% set percent = 100 %}{% endif %}
        <div class="col-lg-4 col-md-6 mb-5">
            <div class="card h-100 shadow border-0 project-card overflow-hidden">
                <div class="position-relative">
                    {% if project.image_path %}
                    <img src="{{ url_for('static', filename='uploads/' ~ project.image_path) }}" class="card-img-top" style="height: 220px; object-fit: cover;" alt="Project Image">
                    {% else %}
                    <div class="bg-secondary text-white d-flex align-items-center justify-content-center" style="height: 220px;">
                        <i class="fas fa-image fa-4x text-light opacity-50"></i>
                    </div>
                    {% endif %}
                    <span class="badge bg-primary position-absolute top-0 end-0 m-3 fs-6 shadow">{{ project.category }}</span>
                </div>
                <div class="card-body d-flex flex-column p-4">
                    <h4 class="card-title fw-bold text-dark mb-2">{{ project.name }}</h4>
                    <p class="text-muted small mb-3"><i class="fas fa-user-tie me-1"></i> {{ project.owner.name }} &nbsp;|&nbsp; <i class="fas fa-clock me-1"></i> {{ project.duration_days }} days</p>
                    <p class="card-text text-secondary mb-4 flex-grow-1">{{ project.description[:120] }}...</p>
                    
                    <div class="mt-auto">
                        <div class="d-flex justify-content-between text-muted fw-bold mb-2">
                            <span class="text-success">${{ '{:,.2f}'.format(project.raised_amount) }}</span>
                            <span>${{ '{:,.2f}'.format(project.goal_amount) }}</span>
                        </div>
                        <div class="progress mb-4" style="height: 12px; border-radius: 6px;">
                            <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" style="width: {{ percent }}%;"></div>
                        </div>
                        
                        <a href="{{ url_for('main.project_detail', project_id=project.id) }}" class="btn btn-outline-primary btn-lg w-100 fw-bold hover-lift">View Investment</a>
                    </div>
                </div>
            </div>
        </div>
    {% else %}
        <div class="col-12 text-center py-5 bg-white rounded shadow-sm">
            <i class="fas fa-box-open fa-4x text-muted mb-3"></i>
            <h3 class="text-muted">No approved projects found.</h3>
            <p class="text-secondary">Be the first to create one by registering as a startup!</p>
        </div>
    {% endfor %}
</div>
{% endblock %}
""",

"templates/project_detail.html": """{% extends 'base.html' %}
{% block content %}
<div class="mb-4">
    <a href="{{ url_for('main.index') }}" class="btn btn-outline-secondary"><i class="fas fa-arrow-left me-2"></i>Back to Projects</a>
</div>
<div class="row">
    <div class="col-lg-8 mb-4">
        <div class="card shadow border-0 overflow-hidden">
            {% if project.image_path %}
            <img src="{{ url_for('static', filename='uploads/' ~ project.image_path) }}" class="card-img-top" style="max-height: 500px; object-fit: cover;">
            {% else %}
            <div class="bg-secondary text-white d-flex align-items-center justify-content-center" style="height: 300px;">
                <i class="fas fa-image fa-4x opacity-50"></i>
            </div>
            {% endif %}
            <div class="card-body p-5">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h1 class="card-title fw-bold text-dark mb-0">{{ project.name }}</h1>
                    <span class="badge bg-primary fs-5 px-3 py-2 shadow-sm">{{ project.category }}</span>
                </div>
                
                <hr class="text-muted">
                <h4 class="fw-bold text-secondary mb-3">About This Project</h4>
                <p class="card-text fs-5 text-dark lh-lg" style="white-space: pre-wrap;">{{ project.description }}</p>
                
                <div class="row mt-5 text-center bg-light p-4 rounded bg-opacity-50">
                    <div class="col-4 border-end">
                        <i class="fas fa-calendar-alt fa-2x text-primary mb-2"></i>
                        <h5 class="fw-bold mb-0">Launched</h5>
                        <p class="text-muted mb-0">{{ project.created_at.strftime('%b %d, %Y') }}</p>
                    </div>
                    <div class="col-4 border-end">
                        <i class="fas fa-clock fa-2x text-warning mb-2"></i>
                        <h5 class="fw-bold mb-0">Duration</h5>
                        <p class="text-muted mb-0">{{ project.duration_days }} Days</p>
                    </div>
                    <div class="col-4">
                        <i class="fas fa-user-tie fa-2x text-info mb-2"></i>
                        <h5 class="fw-bold mb-0">Owner</h5>
                        <p class="text-muted mb-0">{{ project.owner.name }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="col-lg-4">
        <div class="card shadow border-0 p-4 sticky-top bg-light" style="top: 100px;">
            <div class="text-center mb-4">
                <h4 class="fw-bold text-dark text-uppercase letter-spacing-1">Funding Progress</h4>
                {% set percent = (project.raised_amount / project.goal_amount * 100)|round(2) %}
                {% if percent > 100 %}{% set percent = 100 %}{% endif %}
                <div class="display-3 text-success fw-bold my-3">{{ percent }}%</div>
                <p class="text-muted fs-5"><strong class="text-dark">${{ '{:,.2f}'.format(project.raised_amount) }}</strong> raised of ${{ '{:,.2f}'.format(project.goal_amount) }}</p>
            </div>
            
            <div class="progress mb-4 bg-white shadow-sm" style="height: 20px; border-radius: 10px;">
                <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar" style="width: {{ percent }}%;"></div>
            </div>
            
            <div class="d-flex justify-content-between text-muted fw-bold mb-4">
                <span><i class="fas fa-users me-1"></i> {{ project.investments|length }} Investors</span>
                {% set remaining = project.goal_amount - project.raised_amount %}
                {% if remaining > 0 %}
                <span><i class="fas fa-exclamation-circle me-1"></i> ${{ '{:,.2f}'.format(remaining) }} Left</span>
                {% else %}
                <span class="text-success"><i class="fas fa-check-circle me-1"></i> Fully Funded</span>
                {% endif %}
            </div>

            <hr>

            {% if current_user.is_authenticated and current_user.role == 'investor' %}
                {% if remaining > 0 %}
                <a href="{{ url_for('investor.invest', project_id=project.id) }}" class="btn btn-success btn-lg w-100 fw-bold shadow hover-lift py-3 fs-4">
                    <i class="fas fa-hand-holding-usd me-2"></i> Invest Now
                </a>
                {% else %}
                <button class="btn btn-secondary btn-lg w-100 fw-bold shadow py-3" disabled>Goal Reached</button>
                {% endif %}
            {% elif current_user.is_authenticated %}
                <button class="btn btn-outline-secondary btn-lg w-100 fw-bold" disabled>Only investors can invest</button>
            {% else %}
                <a href="{{ url_for('auth.login') }}" class="btn btn-primary btn-lg w-100 fw-bold shadow hover-lift py-3">Login to Invest</a>
            {% endif %}
        </div>
    </div>
</div>
""",

"templates/auth/login.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center mt-5">
    <div class="col-md-5">
        <div class="card shadow border-0 rounded-4 overflow-hidden">
            <div class="card-header bg-primary text-white text-center py-4 border-0">
                <h2 class="mb-0 fw-bold"><i class="fas fa-sign-in-alt me-3"></i>Welcome Back</h2>
                <p class="mb-0 mt-2 text-primary-light">Log in to your FundGrow account</p>
            </div>
            <div class="card-body p-5 bg-light">
                <form method="POST">
                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                    <div class="form-floating mb-4 shadow-sm">
                        <input type="email" name="email" class="form-control focus-ring" id="emailInput" placeholder="name@example.com" required>
                        <label for="emailInput" class="text-muted"><i class="fas fa-envelope me-2"></i>Email Address</label>
                    </div>
                    <div class="form-floating mb-5 shadow-sm">
                        <input type="password" name="password" class="form-control focus-ring" id="pwdInput" placeholder="Password" required>
                        <label for="pwdInput" class="text-muted"><i class="fas fa-lock me-2"></i>Password</label>
                    </div>
                    <button type="submit" class="btn btn-primary btn-lg w-100 fw-bold shadow hover-lift py-3">Log In</button>
                </form>
                <div class="text-center mt-4">
                    <span class="text-secondary">Don't have an account?</span> <a href="{{ url_for('auth.register') }}" class="fw-bold text-primary text-decoration-none">Register here</a>
                </div>
            </div>
        </div>
    </div>
</div>
""",

"templates/auth/register.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-7">
        <div class="card shadow border-0 rounded-4 overflow-hidden">
            <div class="card-header bg-primary text-white text-center py-4 border-0">
                <h2 class="mb-0 fw-bold"><i class="fas fa-user-plus me-3"></i>Join FundGrow</h2>
                <p class="mb-0 mt-2 text-primary-light">Create your account to start investing or raising funds.</p>
            </div>
            <div class="card-body p-5 bg-light">
                <form method="POST">
                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-floating mb-4 shadow-sm">
                                <input type="text" name="name" class="form-control" id="nameInput" placeholder="John Doe" required>
                                <label for="nameInput" class="text-muted"><i class="fas fa-user me-2"></i>Full Name</label>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-floating mb-4 shadow-sm">
                                <input type="text" name="phone" class="form-control" id="phoneInput" placeholder="1234567890">
                                <label for="phoneInput" class="text-muted"><i class="fas fa-phone me-2"></i>Phone Number</label>
                            </div>
                        </div>
                    </div>
                    
                    <div class="form-floating mb-4 shadow-sm">
                        <input type="email" name="email" class="form-control" id="emailInput" placeholder="name@example.com" required>
                        <label for="emailInput" class="text-muted"><i class="fas fa-envelope me-2"></i>Email Address</label>
                    </div>
                    <div class="form-floating mb-4 shadow-sm">
                        <input type="password" name="password" class="form-control" id="pwdInput" placeholder="Password" required>
                        <label for="pwdInput" class="text-muted"><i class="fas fa-lock me-2"></i>Password</label>
                    </div>
                    
                    <div class="mb-5 p-4 bg-white rounded shadow-sm border border-2 border-primary border-opacity-25">
                        <label class="form-label fw-bold text-dark mb-3"><i class="fas fa-users-cog me-2"></i>I want to join as a:</label>
                        <div class="row g-3">
                            <div class="col-md-6">
                                <input type="radio" class="btn-check" name="role" id="roleInvestor" autocomplete="off" value="investor" required checked>
                                <label class="btn btn-outline-primary w-100 py-3 fw-bold" for="roleInvestor">
                                    <i class="fas fa-chart-line fa-2x mb-2 d-block"></i>
                                    Investor<br><small class="fw-normal">I want to fund projects</small>
                                </label>
                            </div>
                            <div class="col-md-6">
                                <input type="radio" class="btn-check" name="role" id="roleStartup" autocomplete="off" value="startup" required>
                                <label class="btn btn-outline-success w-100 py-3 fw-bold" for="roleStartup">
                                    <i class="fas fa-rocket fa-2x mb-2 d-block"></i>
                                    Startup<br><small class="fw-normal">I want to raise funds</small>
                                </label>
                            </div>
                        </div>
                    </div>

                    <button type="submit" class="btn btn-primary btn-lg w-100 fw-bold shadow hover-lift py-3">Create Account</button>
                </form>
                <div class="text-center mt-4">
                    <span class="text-secondary">Already have an account?</span> <a href="{{ url_for('auth.login') }}" class="fw-bold text-primary text-decoration-none">Log in here</a>
                </div>
            </div>
        </div>
    </div>
</div>
""",

"templates/investor/dashboard.html": """{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-lg-3 mb-4">
        <div class="list-group shadow border-0 rounded-3">
            <div class="list-group-item bg-primary text-white fw-bold py-3"><i class="fas fa-user-circle me-2"></i> Investor Panel</div>
            <a href="{{ url_for('investor.dashboard') }}" class="list-group-item list-group-item-action active py-3"><i class="fas fa-home me-2"></i> Dashboard</a>
            <a href="{{ url_for('main.index') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-search-dollar me-2"></i> Browse Projects</a>
            <a href="{{ url_for('investor.history') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-history me-2"></i> Transaction History</a>
        </div>
    </div>
    <div class="col-lg-9">
        <div class="row mb-5">
            <div class="col-md-6 mb-3">
                <div class="card text-white bg-success shadow border-0 rounded-4 overflow-hidden h-100 hover-lift">
                    <div class="card-body p-4 d-flex align-items-center">
                        <div class="rounded-circle bg-white bg-opacity-25 p-3 me-3">
                            <i class="fas fa-wallet fa-3x"></i>
                        </div>
                        <div>
                            <h5 class="card-title text-white-50 text-uppercase fw-bold mb-1">Total Invested</h5>
                            <h2 class="mb-0 fw-bold display-6">${{ '{:,.2f}'.format(total_invested) }}</h2>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-6 mb-3">
                <div class="card text-white bg-info shadow border-0 rounded-4 overflow-hidden h-100 hover-lift">
                    <div class="card-body p-4 d-flex align-items-center">
                        <div class="rounded-circle bg-white bg-opacity-25 p-3 me-3">
                            <i class="fas fa-chart-pie fa-3x"></i>
                        </div>
                        <div>
                            <h5 class="card-title text-white-50 text-uppercase fw-bold mb-1">Total Investments</h5>
                            <h2 class="mb-0 fw-bold display-6">{{ investments|length }}</h2>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h3 class="fw-bold text-dark mb-0"><i class="fas fa-layer-group text-primary me-2"></i>My Portfolio</h3>
        </div>
        
        <div class="card shadow border-0 rounded-4 overflow-hidden">
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0 text-center">
                    <thead class="table-light bg-light">
                        <tr>
                            <th class="py-3 text-start ps-4">Project</th>
                            <th class="py-3">Ownership (%)</th>
                            <th class="py-3">Investment Amount</th>
                            <th class="py-3">Date</th>
                            <th class="py-3 pe-4">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for inv in investments %}
                        <tr>
                            <td class="text-start ps-4 fw-bold">
                                <a href="{{ url_for('main.project_detail', project_id=inv.project_id) }}" class="text-decoration-none text-dark">{{ inv.project.name }}</a>
                            </td>
                            <td><span class="badge bg-primary fs-6">{{ inv.percentage }}%</span></td>
                            <td class="text-success fw-bold">${{ '{:,.2f}'.format(inv.investment_amount) }}</td>
                            <td class="text-muted">{{ inv.created_at.strftime('%Y-%m-%d') }}</td>
                            <td class="pe-4">
                                <a href="{{ url_for('main.project_detail', project_id=inv.project_id) }}" class="btn btn-sm btn-outline-secondary">View</a>
                            </td>
                        </tr>
                        {% else %}
                        <tr>
                            <td colspan="5" class="py-5 text-muted">
                                <i class="fas fa-folder-open fa-3x mb-3 text-secondary opacity-50"></i>
                                <h5>You haven't made any investments yet.</h5>
                                <a href="{{ url_for('main.index') }}" class="btn btn-primary mt-2">Find Projects</a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
""",

"templates/investor/invest.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="card shadow-lg border-0 rounded-4">
            <div class="card-header bg-success text-white py-4 border-0 rounded-top-4 text-center">
                <h2 class="mb-0 fw-bold"><i class="fas fa-seedling me-2"></i>Invest in {{ project.name }}</h2>
            </div>
            <div class="card-body p-5">
                
                <div class="row mb-5 text-center bg-light p-4 rounded-3 border">
                    <div class="col-6 border-end">
                        <small class="text-muted text-uppercase fw-bold">Goal Amount</small>
                        <h3 class="fw-bold text-dark mt-1">${{ '{:,.2f}'.format(project.goal_amount) }}</h3>
                    </div>
                    {% set remaining = project.goal_amount - project.raised_amount %}
                    <div class="col-6">
                        <small class="text-muted text-uppercase fw-bold">Remaining Available</small>
                        <h3 class="fw-bold text-success mt-1">${{ '{:,.2f}'.format(remaining) }}</h3>
                    </div>
                </div>

                <form method="POST">
                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                    <input type="hidden" id="goalAmount" value="{{ project.goal_amount }}">
                    <input type="hidden" id="raisedAmount" value="{{ project.raised_amount }}">
                    <input type="hidden" id="feePercentage" value="{{ platform_fee_percentage }}">
                    
                    <div class="mb-5">
                        <label class="form-label fw-bold fs-5 text-dark"><i class="fas fa-percentage text-primary me-2"></i>Select Ownership Percentage</label>
                        <div class="d-flex align-items-center mb-3">
                            <input type="range" class="form-range flex-grow-1" min="0.01" max="100" step="0.01" id="percentageSlider" name="percentage" value="10">
                            <div class="ms-3 bg-primary text-white px-3 py-2 rounded shadow-sm fw-bold fs-5" style="min-width: 100px; text-align: center;">
                                <span id="percentageOutput">10</span>%
                            </div>
                        </div>
                        
                        <div class="d-flex justify-content-between flex-wrap gap-2 mt-3">
                            <button type="button" class="btn btn-outline-primary flex-fill fw-bold pct-btn" data-pct="5">5%</button>
                            <button type="button" class="btn btn-outline-primary flex-fill fw-bold pct-btn" data-pct="10">10%</button>
                            <button type="button" class="btn btn-outline-primary flex-fill fw-bold pct-btn" data-pct="25">25%</button>
                            <button type="button" class="btn btn-outline-primary flex-fill fw-bold pct-btn" data-pct="50">50%</button>
                            <button type="button" class="btn btn-outline-primary flex-fill fw-bold pct-btn" data-pct="100">100%</button>
                        </div>
                    </div>

                    <div class="card bg-light border-0 mb-4 shadow-sm">
                        <div class="card-body p-4">
                            <h5 class="fw-bold border-bottom pb-2 mb-3 text-secondary">Investment Summary</h5>
                            <div class="d-flex justify-content-between mb-2 fs-5">
                                <span class="text-muted">Investment Amount:</span>
                                <strong class="text-dark" id="calcInvestment">$0.00</strong>
                            </div>
                            <div class="d-flex justify-content-between mb-2 fs-5">
                                <span class="text-muted">Platform Fee ({{ platform_fee_percentage }}%):</span>
                                <strong class="text-danger" id="calcFee">$0.00</strong>
                            </div>
                            <hr class="my-3">
                            <div class="d-flex justify-content-between fs-4">
                                <strong class="text-dark">Total Payable:</strong>
                                <strong class="text-success" id="calcTotal">$0.00</strong>
                            </div>
                            
                            <div id="exceedWarning" class="alert alert-danger mt-3 d-none fw-bold">
                                <i class="fas fa-exclamation-triangle me-2"></i> Amount exceeds remaining available funding!
                            </div>
                        </div>
                    </div>

                    <div class="form-check mb-4 bg-white p-3 border rounded shadow-sm">
                        <input class="form-check-input ms-1 shadow-sm fs-5" type="checkbox" name="agreement" id="agreement" required>
                        <label class="form-check-label ms-3 text-dark pt-1" for="agreement">
                            I understand that crowdfunding involves high risks. I agree to the <a href="#" class="text-primary text-decoration-none">Terms and Conditions</a> and authorize this mock transaction.
                        </label>
                    </div>

                    <div class="d-grid gap-2">
                        <button type="submit" id="submitBtn" class="btn btn-success btn-lg fw-bold shadow-lg py-3 fs-4 hover-lift"><i class="fas fa-lock me-2"></i> Proceed to Secure Payment</button>
                        <a href="{{ url_for('main.project_detail', project_id=project.id) }}" class="btn btn-link text-secondary text-decoration-none mt-2 fw-bold">Cancel</a>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
{% block scripts %}
<script>
    $(document).ready(function() {
        const goalAmount = parseFloat($('#goalAmount').val());
        const raisedAmount = parseFloat($('#raisedAmount').val());
        const feePercentage = parseFloat($('#feePercentage').val());
        const remaining = goalAmount - raisedAmount;
        
        function updateCalculations(pct) {
            const investment = goalAmount * (pct / 100);
            const fee = investment * (feePercentage / 100);
            const total = investment; // In this model, net = investment - fee, but the user pays investment exactly or net?
            // "Investment Amount = Project Goal × Selected Percentage"
            // "Platform Fee = Investment Amount × Platform Fee %"
            // "Net Amount = Investment Amount − Platform Fee"
            // The user invests $Invest, out of which Platform takes $Fee, Startup gets $Net.
            // So Total payable = Investment Amount.
            
            $('#calcInvestment').text('$' + investment.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
            $('#calcFee').text('$' + fee.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
            $('#calcTotal').text('$' + investment.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2}));
            
            if (investment > remaining) {
                $('#exceedWarning').removeClass('d-none');
                $('#submitBtn').prop('disabled', true);
            } else {
                $('#exceedWarning').addClass('d-none');
                $('#submitBtn').prop('disabled', false);
            }
        }
        
        $('#percentageSlider').on('input', function() {
            let val = $(this).val();
            $('#percentageOutput').text(val);
            updateCalculations(val);
        });
        
        $('.pct-btn').click(function() {
            let val = $(this).data('pct');
            $('#percentageSlider').val(val);
            $('#percentageOutput').text(val);
            updateCalculations(val);
        });
        
        // Initial setup to max allowable if remaining ratio is low
        let maxPct = (remaining / goalAmount) * 100;
        if (maxPct < 10) {
            $('#percentageSlider').val(maxPct.toFixed(2));
            $('#percentageOutput').text(maxPct.toFixed(2));
            updateCalculations(maxPct);
        } else {
            $('#percentageSlider').val(10);
            $('#percentageOutput').text('10');
            updateCalculations(10);
        }
    });
</script>
{% endblock %}
"""
}

# continuing in the next one to avoid long string issues.
for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Setup templates part 1 done.")
