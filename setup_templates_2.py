import os

base_dir = "D:/fundgrow"

files = {
"templates/investor/payment.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center">
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-header bg-primary text-white text-center py-3">
                <h3 class="mb-0"><i class="fas fa-credit-card me-2"></i>Mock Payment Gateway</h3>
            </div>
            <div class="card-body p-4">
                <div class="alert alert-info border-info border-2 bg-info bg-opacity-10 shadow-sm border-start">
                    <h5 class="fw-bold"><i class="fas fa-info-circle me-2"></i>Payment Details</h5>
                    <ul class="list-unstyled mb-0 fs-5 mt-3">
                        <li class="mb-2"><strong class="text-dark">Project:</strong> <span class="text-primary">{{ project.name }}</span></li>
                        <li class="mb-2"><strong class="text-dark">Ownership Split:</strong> <span class="badge bg-secondary">{{ percentage }}%</span></li>
                        <li><strong class="text-dark">Total Amount Due:</strong> <span class="text-success fw-bold">${{ '{:,.2f}'.format(investment_amount) }}</span></li>
                    </ul>
                </div>
                
                <form action="{{ url_for('investor.process_payment', project_id=project.id) }}" method="POST" class="mt-4 shadow-sm p-4 rounded bg-light border">
                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                    <input type="hidden" name="percentage" value="{{ percentage }}">
                    
                    <h5 class="fw-bold text-secondary mb-3 border-bottom pb-2">Credit Card Information</h5>
                    <div class="form-floating mb-3 shadow-sm">
                        <input type="text" class="form-control focus-ring text-muted" id="cardInput" placeholder="xxxx-xxxx-xxxx-xxxx" value="1234-5678-9012-3456" readonly style="cursor: not-allowed; background-color: #e9ecef;">
                        <label for="cardInput"><i class="far fa-credit-card me-2"></i>Card Number (Mock)</label>
                    </div>
                    
                    <div class="row">
                        <div class="col-6">
                            <div class="form-floating mb-3 shadow-sm">
                                <input type="text" class="form-control focus-ring text-muted" id="expInput" placeholder="MM/YY" value="12/30" readonly style="cursor: not-allowed; background-color: #e9ecef;">
                                <label for="expInput"><i class="far fa-calendar-alt me-2"></i>Expiry Date</label>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="form-floating mb-4 shadow-sm">
                                <input type="text" class="form-control focus-ring text-muted" id="cvcInput" placeholder="123" value="123" readonly style="cursor: not-allowed; background-color: #e9ecef;">
                                <label for="cvcInput"><i class="fas fa-lock me-2"></i>CVC</label>
                            </div>
                        </div>
                    </div>
                    
                    <button type="submit" class="btn btn-success btn-lg w-100 fw-bold shadow hover-lift py-3"><i class="fas fa-check-circle me-2"></i> Confirm Payment of ${{ '{:,.2f}'.format(investment_amount) }}</button>
                    <a href="{{ url_for('investor.invest', project_id=project.id) }}" class="btn btn-link w-100 mt-2 text-decoration-none text-secondary fw-bold">Cancel Transaction</a>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

"templates/investor/success.html": """{% extends 'base.html' %}
{% block content %}
<div class="row justify-content-center text-center">
    <div class="col-md-8">
        <div class="card shadow-lg border-0 rounded-4 mt-5">
            <div class="card-body p-5">
                <div class="text-success mb-4 rounded-circle bg-success bg-opacity-10 d-inline-block p-4">
                    <i class="fas fa-check-circle fa-5x"></i>
                </div>
                <h1 class="display-5 fw-bold text-dark mb-3">Investment Successful!</h1>
                <p class="fs-4 text-muted mb-5">Thank you, {{ current_user.name }}. Your transaction has been securely processed.</p>
                
                <div class="bg-light p-4 rounded-3 text-start mb-5 shadow-inner border">
                    <h4 class="fw-bold mb-4 text-secondary border-bottom pb-2"><i class="fas fa-receipt me-2 text-primary"></i>Transaction Receipt</h4>
                    <div class="row mb-3 fs-5">
                        <div class="col-6 text-muted">Transaction Ref:</div>
                        <div class="col-6 fw-bold text-dark d-flex align-items-center">
                            {{ transaction.transaction_reference }}
                            <button class="btn btn-sm btn-outline-secondary ms-2" onclick="navigator.clipboard.writeText('{{ transaction.transaction_reference }}')" title="Copy Reference"><i class="far fa-copy"></i></button>
                        </div>
                    </div>
                    <div class="row mb-3 fs-5">
                        <div class="col-6 text-muted">Project:</div>
                        <div class="col-6 fw-bold text-primary">{{ project.name }}</div>
                    </div>
                    <div class="row mb-3 fs-5">
                        <div class="col-6 text-muted">Ownership Equity:</div>
                        <div class="col-6 fw-bold"><span class="badge bg-secondary fs-6">{{ transaction.amount / project.goal_amount * 100 }}%</span></div>
                    </div>
                    <div class="row mb-3 fs-5">
                        <div class="col-6 text-muted">Amount Invested:</div>
                        <div class="col-6 fw-bold text-success">${{ '{:,.2f}'.format(transaction.amount) }}</div>
                    </div>
                </div>
                
                <div class="d-grid gap-3 d-sm-flex justify-content-sm-center">
                    <a href="{{ url_for('investor.dashboard') }}" class="btn btn-primary btn-lg px-4 gap-3 fw-bold shadow hover-lift"><i class="fas fa-home me-2"></i> Go to Dashboard</a>
                    <a href="{{ url_for('main.index') }}" class="btn btn-outline-secondary btn-lg px-4 fw-bold hover-lift"><i class="fas fa-search me-2"></i> Browse More Projects</a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

"templates/investor/history.html": """{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-lg-3 mb-4">
        <div class="list-group shadow border-0 rounded-3">
            <div class="list-group-item bg-primary text-white fw-bold py-3"><i class="fas fa-user-circle me-2"></i> Investor Panel</div>
            <a href="{{ url_for('investor.dashboard') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-home me-2"></i> Dashboard</a>
            <a href="{{ url_for('main.index') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-search-dollar me-2"></i> Browse Projects</a>
            <a href="{{ url_for('investor.history') }}" class="list-group-item list-group-item-action active py-3"><i class="fas fa-history me-2"></i> Transaction History</a>
        </div>
    </div>
    <div class="col-lg-9">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h3 class="fw-bold text-dark mb-0"><i class="fas fa-receipt text-primary me-2"></i>Transaction Ledger</h3>
            <button class="btn btn-outline-secondary" onclick="window.print()"><i class="fas fa-print me-2"></i>Print/Export</button>
        </div>
        <div class="card shadow border-0 rounded-4 overflow-hidden">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover table-striped align-middle mb-0">
                        <thead class="table-dark">
                            <tr>
                                <th class="py-3 ps-4">Date</th>
                                <th class="py-3">Reference ID</th>
                                <th class="py-3">Project</th>
                                <th class="py-3 text-end pe-4">Amount Paid</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for txn in transactions %}
                            <tr>
                                <td class="ps-4 text-muted"><i class="far fa-calendar me-1"></i> {{ txn.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                                <td><code class="text-secondary bg-light px-2 py-1 rounded">{{ txn.transaction_reference[:12] }}...</code></td>
                                <td class="fw-bold"><a href="{{ url_for('main.project_detail', project_id=txn.project_id) }}" class="text-decoration-none text-dark">{{ txn.project.name }}</a></td>
                                <td class="text-end pe-4 text-success fw-bold">${{ '{:,.2f}'.format(txn.amount) }}</td>
                            </tr>
                            {% else %}
                            <tr>
                                <td colspan="4" class="text-center py-5 text-muted">
                                    <i class="fas fa-file-invoice-dollar fa-3x mb-3 text-secondary opacity-50"></i>
                                    <h5>No transactions found.</h5>
                                    <p>Start investing to build your transaction history.</p>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

"templates/startup/dashboard.html": """{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-lg-3 mb-4">
        <div class="list-group shadow border-0 rounded-3">
            <div class="list-group-item bg-success text-white fw-bold py-3"><i class="fas fa-rocket me-2"></i> Startup Hub</div>
            <a href="{{ url_for('startup.dashboard') }}" class="list-group-item list-group-item-action active py-3"><i class="fas fa-home me-2"></i> My Dashboard</a>
            <a href="{{ url_for('startup.add_project') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-plus-circle me-2"></i> Launch New Project</a>
        </div>
    </div>
    <div class="col-lg-9">
        <div class="card bg-primary text-white shadow border-0 rounded-4 overflow-hidden mb-5 hover-lift">
            <div class="card-body p-5 d-flex align-items-center justify-content-between">
                <div>
                    <h5 class="text-uppercase text-white-50 fw-bold mb-2">Total Funds Raised</h5>
                    <h1 class="display-3 fw-bold mb-0">${{ '{:,.2f}'.format(total_raised) }}</h1>
                </div>
                <div class="rounded-circle bg-white bg-opacity-25 p-4 d-none d-md-block">
                    <i class="fas fa-hand-holding-usd fa-4x text-light"></i>
                </div>
            </div>
        </div>
        
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h3 class="fw-bold text-dark mb-0"><i class="fas fa-project-diagram text-success me-2"></i>My Projects Portfolio</h3>
            <a href="{{ url_for('startup.add_project') }}" class="btn btn-success fw-bold shadow"><i class="fas fa-plus me-2"></i>New Pitch</a>
        </div>
        
        <div class="row">
            {% for project in projects %}
            {% set percent = (project.raised_amount / project.goal_amount * 100)|round(2) %}
            {% if percent > 100 %}{% set percent = 100 %}{% endif %}
            <div class="col-md-6 mb-4">
                <div class="card shadow border-0 rounded-4 overflow-hidden h-100 hover-lift">
                    <div class="card-body p-4 position-relative">
                        {% if project.status == 'approved' %}
                            <span class="badge bg-success position-absolute top-0 end-0 m-3 fs-6 px-3 shadow-sm"><i class="fas fa-check-circle me-1"></i> Live</span>
                        {% elif project.status == 'pending' %}
                            <span class="badge bg-warning text-dark position-absolute top-0 end-0 m-3 fs-6 px-3 shadow-sm"><i class="fas fa-hourglass-half me-1"></i> Under Review</span>
                        {% else %}
                            <span class="badge bg-danger position-absolute top-0 end-0 m-3 fs-6 px-3 shadow-sm"><i class="fas fa-times-circle me-1"></i> Rejected</span>
                        {% endif %}
                        
                        <h4 class="fw-bold text-dark mb-1 w-75 text-truncate">{{ project.name }}</h4>
                        <p class="text-muted small mb-4 font-monospace"><i class="far fa-calendar me-1"></i> Launched {{ project.created_at.strftime('%b %d, %Y') }}</p>
                        
                        <div class="d-flex justify-content-between fw-bold mb-2 fs-5">
                            <span class="text-success">${{ '{:,.0f}'.format(project.raised_amount) }}</span>
                            <span class="text-secondary">/ ${{ '{:,.0f}'.format(project.goal_amount) }}</span>
                        </div>
                        <div class="progress mb-4 bg-light shadow-inner" style="height: 12px; border-radius: 6px;">
                            <div class="progress-bar progress-bar-striped progress-bar-animated {% if project.status=='approved' %}bg-success{%else%}bg-secondary{%endif%}" role="progressbar" style="width: {{ percent }}%;"></div>
                        </div>
                        
                        <div class="d-flex justify-content-between align-items-center mt-auto border-top pt-3">
                            <span class="text-muted fw-bold"><i class="fas fa-chart-line me-1"></i> {{ percent }}% Funded</span>
                            <a href="{{ url_for('main.project_detail', project_id=project.id) }}" class="btn btn-outline-primary btn-sm fw-bold">View Page</a>
                        </div>
                    </div>
                </div>
            </div>
            {% else %}
            <div class="col-12 text-center py-5 bg-white rounded shadow-sm border">
                <i class="fas fa-rocket fa-4x text-muted mb-3 opacity-50"></i>
                <h3 class="text-muted">No projects launched yet.</h3>
                <p class="text-secondary">Time to bring your idea to life!</p>
                <a href="{{ url_for('startup.add_project') }}" class="btn btn-success btn-lg mt-3 shadow"><i class="fas fa-plus-circle me-2"></i> Start Your First Campaign</a>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
{% endblock %}
""",

"templates/startup/add_project.html": """{% extends 'base.html' %}
{% block content %}
<div class="row">
    <div class="col-lg-3 mb-4">
        <div class="list-group shadow border-0 rounded-3">
            <div class="list-group-item bg-success text-white fw-bold py-3"><i class="fas fa-rocket me-2"></i> Startup Hub</div>
            <a href="{{ url_for('startup.dashboard') }}" class="list-group-item list-group-item-action py-3"><i class="fas fa-home me-2"></i> My Dashboard</a>
            <a href="{{ url_for('startup.add_project') }}" class="list-group-item list-group-item-action active py-3"><i class="fas fa-plus-circle me-2"></i> Launch New Project</a>
        </div>
    </div>
    <div class="col-lg-9">
        <div class="card shadow-lg border-0 rounded-4">
            <div class="card-header bg-white border-bottom-0 py-4 px-5 pb-0">
                <h2 class="mb-0 fw-bold text-dark"><i class="fas fa-bullhorn text-success me-3"></i>Create Pitch</h2>
                <p class="text-muted mt-2">Fill in the details below to launch your startup campaign.</p>
            </div>
            <div class="card-body p-5 pt-4">
                <form method="POST" enctype="multipart/form-data">
                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
                    
                    <div class="form-floating mb-4 shadow-sm">
                        <input type="text" name="name" class="form-control focus-ring text-dark fw-bold focus-ring-success fs-5" id="nameInput" placeholder="Project Name" required>
                        <label for="nameInput" class="text-muted"><i class="fas fa-tag me-2"></i>Project Title</label>
                    </div>
                    
                    <div class="mb-4 shadow-sm rounded border p-1 focus-ring-target">
                        <textarea name="description" class="form-control border-0 focus-ring-none shadow-none" rows="5" placeholder="Describe your startup vision, market potential, and required funding use..." required></textarea>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-floating mb-4 shadow-sm">
                                <input type="number" name="goal_amount" class="form-control text-success fw-bold fs-5" id="amtInput" min="100" step="0.01" placeholder="10000" required>
                                <label for="amtInput" class="text-muted"><i class="fas fa-dollar-sign me-2"></i>Funding Goal ($)</label>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="form-floating mb-4 shadow-sm">
                                <input type="number" name="duration_days" class="form-control fs-5" id="durInput" min="1" max="365" placeholder="30" required>
                                <label for="durInput" class="text-muted"><i class="fas fa-clock me-2"></i>Campaign Duration (Days)</label>
                            </div>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-floating mb-4 shadow-sm">
                                <select name="category" class="form-select fs-5" id="catInput" required>
                                    <option value="" disabled selected>Select Category</option>
                                    <option value="Technology">Technology</option>
                                    <option value="Health">Health & MedTech</option>
                                    <option value="Finance">FinTech</option>
                                    <option value="Education">EdTech</option>
                                    <option value="Environment">Green/Eco</option>
                                    <option value="Other">Other</option>
                                </select>
                                <label for="catInput" class="text-muted"><i class="fas fa-list me-2"></i>Category</label>
                            </div>
                        </div>
                        <div class="col-md-6">
                            <div class="mb-4">
                                <label class="form-label fw-bold text-muted small mb-1 ms-1"><i class="fas fa-image me-1"></i> Cover Image</label>
                                <input type="file" name="image" class="form-control form-control-lg shadow-sm" accept="image/*">
                            </div>
                        </div>
                    </div>
                    
                    <hr class="my-4">
                    <button type="submit" class="btn btn-success btn-lg w-100 fw-bold shadow hover-lift py-3 fs-4"><i class="fas fa-paper-plane me-2"></i> Submit for Review</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}
"""
}

for path, content in files.items():
    full_path = os.path.join(base_dir, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

print("Setup templates part 2 done.")
