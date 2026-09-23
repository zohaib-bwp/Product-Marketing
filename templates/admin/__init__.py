{% extends "base.html" %}
{% block title %}Register{% endblock %}
{% block content %}
<div class="row justify-content-center mt-5">
  <div class="col-md-6">
    <div class="card">
      <div class="card-body p-4">
        <h3 class="text-center">Register</h3>
        <form method="post" action="/api/register">
          <div class="mb-3"><label class="form-label">Name</label><input class="form-control" name="name" required></div>
          <div class="mb-3"><label class="form-label">Email</label><input class="form-control" type="email" name="email" required></div>
          <div class="mb-3"><label class="form-label">Phone</label><input class="form-control" name="phone" required></div>
          <div class="mb-3"><label class="form-label">Address</label><textarea class="form-control" name="address"></textarea></div>
          <div class="mb-3"><label class="form-label">Password</label><input class="form-control" type="password" name="password" required></div>
          <button class="btn btn-success w-100">Create Account</button>
        </form>
      </div>
    </div>
  </div>
</div>
{% endblock %}
