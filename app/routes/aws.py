"""AWS connection routes."""
from flask import Blueprint, request, redirect, url_for, flash, render_template
from app.services.aws_service import AWSService
from app.routes.auth import login_required

aws_bp = Blueprint('aws', __name__, url_prefix='/aws')
aws_service = AWSService()


@aws_bp.route('/connect', methods=['POST'])
@login_required
def connect():
    """Handle AWS credential submission and validation."""
    access_key = request.form.get('access_key', '').strip()
    secret_key = request.form.get('secret_key', '').strip()
    region = request.form.get('region', 'us-west-2').strip()
    
    # Validate input
    if not access_key or not secret_key:
        flash('AWS Access Key and Secret Key are required.', 'error')
        return redirect(url_for('auth.dashboard'))
    
    if not region:
        region = 'us-west-2'
    
    # Validate credentials with AWS
    if aws_service.validate_credentials(access_key, secret_key, region):
        # Store encrypted credentials in session
        aws_service.store_credentials(access_key, secret_key, region)
        flash(f'Successfully connected to AWS in region {region}!', 'success')
    else:
        flash('Invalid AWS credentials. Please check your Access Key and Secret Key.', 'error')
    
    return redirect(url_for('auth.dashboard'))


@aws_bp.route('/disconnect')
@login_required
def disconnect():
    """Clear AWS credentials from session."""
    aws_service.clear_credentials()
    flash('Disconnected from AWS.', 'info')
    return redirect(url_for('auth.dashboard'))
