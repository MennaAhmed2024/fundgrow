import os

base_dir = "D:/fundgrow"

files = {
"templates/admin/dashboard.html": """{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-lg-3 mb-4">
        <div class="list-group shadow border-0 rounded-3">
            <div class="list-group-item bg-dark text-white fw-bold py-3"><i class="fas fa-shield-alt me-2"></i> Admin Panel</div>
            <a href="{{ url_for('admin.dashboard') }}" class="list-group-item list-group-item-action active py-3"><i class="fas fa-chart-line me-2"></i> Dashboard</a>
            <a href="{{ url_for('admin.pending_projects') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-clock me-2"></i> Pending Projects</a>
            <a href="{{ url_for('admin.published_projects') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-check-double me-2"></i> Published Projects</a>
            <a href="{{ url_for('admin.users_management') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-users me-2"></i> Manage Users</a>
            <a href="{{ url_for('admin.all_transactions') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-money-bill-wave me-2"></i> All Transactions</a>
            <a href="{{ url_for('admin.settings') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-cog me-2"></i> Platform Settings</a>
        </div>
    </div>
    <div class="col-lg-9">
        <div class="row mb-4">
            <div class="col-md-4 mb-3">
                <div class="card bg-primary text-white shadow border-0 h-100 hover-lift rounded-4">
                    <div class="card-body p-4 text-center">
                        <i class="fas fa-project-diagram fa-3x mb-3 opacity-75"></i>
                        <h5 class="fw-bold mb-1 text-uppercase text-white-50">Total Projects</h5>
                        <h2 class="display-5 fw-bold mb-0">{{ projects_count }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card bg-success text-white shadow border-0 h-100 hover-lift rounded-4">
                    <div class="card-body p-4 text-center">
                        <i class="fas fa-users fa-3x mb-3 opacity-75"></i>
                        <h5 class="fw-bold mb-1 text-uppercase text-white-50">Active Users</h5>
                        <h2 class="display-5 fw-bold mb-0">{{ users_count }}</h2>
                    </div>
                </div>
            </div>
            <div class="col-md-4 mb-3">
                <div class="card bg-dark text-white shadow border-0 h-100 hover-lift rounded-4">
                    <div class="card-body p-4 text-center">
                        <i class="fas fa-coins fa-3x mb-3 text-warning"></i>
                        <h5 class="fw-bold mb-1 text-uppercase text-white-50">Platform Revenue</h5>
                        <h2 class="display-5 fw-bold mb-0 text-warning">${{ '{:,.0f}'.format(total_fee) }}</h2>
                    </div>
                </div>
            </div>
        </div>

        <h4 class="fw-bold text-dark mb-3"><i class="fas fa-history text-secondary me-2"></i>Recent Transactions</h4>
        <div class="card shadow border-0 rounded-4 overflow-hidden">
            <div class="table-responsive">
                <table class="table table-hover align-middle mb-0">
                    <thead class="table-light">
                        <tr>
                            <th class="py-3 ps-4">Ref</th>
                            <th class="py-3">Amount</th>
                            <th class="py-3 text-danger">Fee Earned</th>
                            <th class="py-3 text-success">Net Transfer</th>
                            <th class="py-3 pe-4">Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for t in transactions %}
                        <tr>
                            <td class="ps-4 fw-bold"><code>{{ t.transaction_reference[:8] }}</code></td>
                            <td class="fw-bold">${{ '{:,.2f}'.format(t.amount) }}</td>
                            <td class="text-danger fw-bold">+${{ '{:,.2f}'.format(t.platform_fee) }}</td>
                            <td class="text-success fw-bold">${{ '{:,.2f}'.format(t.transferred_amount) }}</td>
                            <td class="pe-4 text-muted small"><i class="far fa-clock me-1"></i>{{ t.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                        </tr>
                        {% else %}
                        <tr><td colspan="5" class="py-4 text-center text-muted">No transactions found.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

"templates/admin/pending_projects.html": """{% extends 'base.html' %}
{% block content %}
<div class="row">
    <!-- Sidebar omitted for brevity, adding a quick back button -->
    <div class="col-12 mb-3">
        <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline-dark"><i class="fas fa-arrow-left me-2"></i>Back to Dashboard</a>
    </div>
    <div class="col-12">
        <h3 class="fw-bold text-dark mb-4"><i class="fas fa-clock text-warning me-2"></i>Pending Approvals</h3>
        <div class="card shadow border-0 rounded-4 overflow-hidden">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                    <tr>
                        <th class="py-3 ps-4">Project Title</th>
                        <th>Startup Owner</th>
                        <th>Goal Set</th>
                        <th>Category</th>
                        <th class="pe-4 text-center">Action</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in projects %}
                    <tr>
                        <td class="ps-4 fw-bold"><a href="{{ url_for('main.project_detail', project_id=p.id) }}" target="_blank" class="text-dark">{{ p.name }} <i class="fas fa-external-link-alt small text-muted"></i></a></td>
                        <td>{{ p.owner.name }}</td>
                        <td class="text-success fw-bold">${{ '{:,.0f}'.format(p.goal_amount) }}</td>
                        <td><span class="badge bg-secondary">{{ p.category }}</span></td>
                        <td class="pe-4 text-center">
                            <a href="{{ url_for('admin.project_action', project_id=p.id, action='approve') }}" class="btn btn-sm btn-success fw-bold shadow-sm me-1"><i class="fas fa-check"></i> Approve</a>
                            <a href="{{ url_for('admin.project_action', project_id=p.id, action='reject') }}" class="btn btn-sm btn-danger fw-bold shadow-sm"><i class="fas fa-times"></i> Reject</a>
                        </td>
                    </tr>
                    {% else %}
                    <tr><td colspan="5" class="py-5 text-center text-muted"><i class="fas fa-check-circle fa-3x mb-3 text-success opacity-50"></i><h5>All caught up! No pending projects.</h5></td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""",

"templates/admin/published_projects.html": """{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-12 mb-3">
        <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline-dark"><i class="fas fa-arrow-left me-2"></i>Back to Dashboard</a>
    </div>
    <div class="col-12">
        <h3 class="fw-bold text-dark mb-4"><i class="fas fa-check-double text-success me-2"></i>Published Projects</h3>
        <div class="card shadow border-0 rounded-4 overflow-hidden">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                    <tr>
                        <th class="py-3 ps-4">Project</th>
                        <th>Status</th>
                        <th>Goal</th>
                        <th>Raised</th>
                        <th class="pe-4">Progress</th>
                    </tr>
                </thead>
                <tbody>
                    {% for p in projects %}
                    {% set pct = (p.raised_amount/p.goal_amount*100)|round(1) %}
                    {% if pct>100 %}{% set pct=100 %}{% endif %}
                    <tr>
                        <td class="ps-4 fw-bold"><a href="{{ url_for('main.project_detail', project_id=p.id) }}" target="_blank" class="text-decoration-none text-dark">{{ p.name }}</a></td>
                        <td><span class="badge bg-success">Live</span></td>
                        <td class="text-muted fw-bold">${{ '{:,.0f}'.format(p.goal_amount) }}</td>
                        <td class="text-success fw-bold">${{ '{:,.0f}'.format(p.raised_amount) }}</td>
                        <td class="pe-4 w-25">
                            <div class="progress" style="height: 10px;">
                                <div class="progress-bar bg-success" style="width:{{ pct }}%"></div>
                            </div>
                        </td>
                    </tr>
                    {% else %}
                    <tr><td colspan="5" class="py-4 text-center text-muted">No published projects yet.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""",

"templates/admin/users.html": """{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-12 mb-3">
        <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline-dark"><i class="fas fa-arrow-left me-2"></i>Back to Dashboard</a>
    </div>
    <div class="col-12">
        <h3 class="fw-bold text-dark mb-4"><i class="fas fa-users-cog text-primary me-2"></i>Manage Users</h3>
        <div class="card shadow border-0 rounded-4 overflow-hidden">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                    <tr>
                        <th class="py-3 ps-4">Name</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Joined</th>
                        <th class="pe-4 text-center">Items</th>
                    </tr>
                </thead>
                <tbody>
                    {% for u in users %}
                    <tr>
                        <td class="ps-4 fw-bold text-dark"><i class="fas fa-user-circle me-2 text-muted"></i>{{ u.name }}</td>
                        <td class="text-muted">{{ u.email }}</td>
                        <td>
                            {% if u.role == 'startup' %}<span class="badge bg-success">Startup</span>{% else %}<span class="badge bg-primary">Investor</span>{% endif %}
                        </td>
                        <td class="text-muted small">{{ u.created_at.strftime('%Y-%m-%d') }}</td>
                        <td class="pe-4 text-center fw-bold">
                            {% if u.role == 'startup' %}
                            <span class="text-success"><i class="fas fa-rocket me-1"></i>{{ u.projects|length }} Projects</span>
                            {% else %}
                            <span class="text-primary"><i class="fas fa-chart-line me-1"></i>{{ u.investments|length }} Inv.</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% else %}
                    <tr><td colspan="5" class="py-4 text-center text-muted">No users found.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""",

"templates/admin/transactions.html": """{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-12 mb-3">
        <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline-dark"><i class="fas fa-arrow-left me-2"></i>Back to Dashboard</a>
    </div>
    <div class="col-12">
        <h3 class="fw-bold text-dark mb-4"><i class="fas fa-money-bill-wave text-success me-2"></i>Global Ledger</h3>
        <div class="card shadow border-0 rounded-4 overflow-hidden">
            <table class="table table-hover table-striped align-middle mb-0 text-center">
                <thead class="table-dark">
                    <tr>
                        <th class="py-3 ps-4 text-start">Date</th>
                        <th class="py-3 text-start">Reference</th>
                        <th class="py-3 text-start">Project / Investor</th>
                        <th class="py-3 text-end">Gross Inv.</th>
                        <th class="py-3 text-danger text-end">Platf. Fee</th>
                        <th class="py-3 text-success text-end pe-4">Net Amount</th>
                    </tr>
                </thead>
                <tbody>
                    {% for txn in transactions %}
                    <tr>
                        <td class="ps-4 text-start text-muted small"><i class="far fa-calendar me-1"></i> {{ txn.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                        <td class="text-start"><code>{{ txn.transaction_reference[:8] }}...</code></td>
                        <td class="text-start">
                            <span class="fw-bold text-dark">{{ txn.project.name }}</span><br>
                            <small class="text-muted">By UserId: {{ txn.investor_id }}</small>
                        </td>
                        <td class="text-end fw-bold">${{ '{:,.2f}'.format(txn.amount) }}</td>
                        <td class="text-end text-danger fw-bold">-${{ '{:,.2f}'.format(txn.platform_fee) }}</td>
                        <td class="text-end text-success fw-bold pe-4">${{ '{:,.2f}'.format(txn.transferred_amount) }}</td>
                    </tr>
                    {% else %}
                    <tr><td colspan="6" class="py-5 text-center text-muted">No transactions recorded yet.</td></tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
""",

"templates/admin/settings.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6 mb-3">
        <a href="{{ url_for('admin.dashboard') }}" class="btn btn-outline-dark"><i class="fas fa-arrow-left me-2"></i>Back to Dashboard</a>
    </div>
    <div class="w-100 mt-2"></div>
    <div class="col-md-6">
        <div class="card shadow border-0 rounded-4">
            <div class="card-header bg-dark text-white border-0 py-4 text-center">
                <h3 class="mb-0 fw-bold"><i class="fas fa-cogs me-3"></i>Platform Settings</h3>
            </div>
            <div class="card-body p-5 bg-light">
                <form method="POST">
                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                    
                    <div class="alert alert-warning border border-warning shadow-sm mb-4">
                        <h5 class="fw-bold text-dark"><i class="fas fa-exclamation-triangle text-warning me-2"></i>Critical Setting</h5>
                        <p class="mb-0 text-muted small">Changing the platform fee directly affects future transactions. It automatically recalculates the net amounts transferred to startups.</p>
                    </div>

                    <label class="form-label fw-bold text-dark fs-5 mb-3"><i class="fas fa-percentage text-primary me-2"></i>Global Platform Commission Fee</label>
                    <div class="input-group input-group-lg mb-4 shadow-sm">
                        <span class="input-group-text bg-white border-end-0 text-success"><i class="fas fa-chart-line"></i></span>
                        <input type="number" step="0.01" min="0" max="100" name="fee" class="form-control border-start-0 fw-bold text-dark" value="{{ setting.platform_fee_percentage if setting else 10.00 }}" required>
                        <span class="input-group-text bg-dark text-white fw-bold border-dark">%</span>
                    </div>
                    
                    <button type="submit" class="btn btn-primary btn-lg w-100 fw-bold shadow hover-lift py-3"><i class="fas fa-save me-2"></i> Update Settings</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

"static/css/style.css": """
/* ----------------------------------
   Core Layout & Basic Overrides 
----------------------------------- */
body {
    background-color: #f8f9fa;
    font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}
.main-content {
    flex: 1;
}

/* ----------------------------------
   Navbar Styling 
----------------------------------- */
.navbar {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%) !important;
}

/* ----------------------------------
   Card Variations & Hover Effects 
----------------------------------- */
.card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.hover-lift:hover {
    transform: translateY(-8px);
    box-shadow: 0 1rem 3rem rgba(0,0,0,.15) !important;
}

.project-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 .5rem 1rem rgba(0,0,0,.15) !important;
}

/* ----------------------------------
   Custom Utility Classes 
----------------------------------- */
.z-index-1 {
    z-index: 1;
}
.letter-spacing-1 {
    letter-spacing: 1px;
}
.shadow-inner {
    box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
}

/* ----------------------------------
   Focus Ring Helpers
----------------------------------- */
.focus-ring:focus {
    border-color: #86b7fe;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}
.focus-ring-success:focus {
    border-color: #75b798;
    box-shadow: 0 0 0 0.25rem rgba(25, 135, 84, 0.25);
}
.focus-ring-target:focus-within {
    border-color: #86b7fe !important;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25) !important;
}
.focus-ring-none {
    outline: none !important;
}
""",

"static/js/main.js": """
// Custom JavaScript for FundGrow Platform 
$(document).ready(function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        $('.alert-dismissible').fadeOut('fast');
    }, 5000);
});
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Setup templates part 3 done.")
