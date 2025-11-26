"""IAM display routes."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.services.iam_service import IAMService
from app.routes.auth import login_required
from app.utils.pagination import paginate
from botocore.exceptions import ClientError

iam_bp = Blueprint('iam', __name__, url_prefix='/iam')
iam_service = IAMService()


@iam_bp.route('/users')
@login_required
def users():
    """Display all IAM users with pagination."""
    try:
        # Get page number from query string
        page = request.args.get('page', 1, type=int)
        
        # Get all users
        all_users = iam_service.get_all_users()
        
        # Paginate results
        paginated = paginate(all_users, page=page, per_page=50)
        
        return render_template('users.html', paginated=paginated)
        
    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('auth.dashboard'))
    except ClientError as e:
        error_message = e.response['Error']['Message']
        flash(f'AWS Error: {error_message}', 'error')
        return redirect(url_for('auth.dashboard'))
    except Exception as e:
        flash(f'Unexpected error: {str(e)}', 'error')
        return redirect(url_for('auth.dashboard'))


@iam_bp.route('/roles')
@login_required
def roles():
    """Display all IAM roles with pagination."""
    try:
        # Get page number from query string
        page = request.args.get('page', 1, type=int)
        
        # Get all roles
        all_roles = iam_service.get_all_roles()
        
        # Paginate results
        paginated = paginate(all_roles, page=page, per_page=50)
        
        return render_template('roles.html', paginated=paginated)
        
    except ValueError as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('auth.dashboard'))
    except ClientError as e:
        error_message = e.response['Error']['Message']
        flash(f'AWS Error: {error_message}', 'error')
        return redirect(url_for('auth.dashboard'))
    except Exception as e:
        flash(f'Unexpected error: {str(e)}', 'error')
        return redirect(url_for('auth.dashboard'))
