function openEditStaffForm(staffId) {
    fetch(`/get_staff/${staffId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('edit_staff_id').value = data.id;
            document.getElementById('edit_first_name').value = data.first_name;
            document.getElementById('edit_last_name').value = data.last_name;
            document.getElementById('edit_position').value = data.position;
            document.getElementById('edit_role').value = data.role;

            var editStaffModal = new bootstrap.Modal(document.getElementById('editStaffModal'));
            editStaffModal.show();
        });
}

document.getElementById('form_edit_staff').addEventListener('submit', function(event) {
    event.preventDefault();

    const staffId = document.getElementById('edit_staff_id').value;
    const firstName = document.getElementById('edit_first_name').value;
    const lastName = document.getElementById('edit_last_name').value;
    const position = document.getElementById('edit_position').value;
    const role = document.getElementById('edit_role').value;

    const formData = new FormData();
    formData.append('staff_id', staffId);
    formData.append('first_name', firstName);
    formData.append('last_name', lastName);
    formData.append('position', position);
    formData.append('role', role);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch(`/edit_staff/${staffId}/`, {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('Error updating staff');
        }
    });
});

function confirmDeleteStaff(staffId) {
    if (confirm("Are you sure you want to delete this staff?")) {
        deleteStaff(staffId);
    }
}

function deleteStaff(staffId) {
    fetch(`/delete_staff/${staffId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            // Remove the deleted staff from the page
            document.getElementById(`staff_${staffId}`).remove();
        } else {
            alert('Error deleting staff: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while trying to delete the staff.');
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}