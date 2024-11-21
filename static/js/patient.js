function openEditPatientForm(patientId) {
    fetch(`/get_patient/${patientId}/`)
        .then(response => response.json())
        .then(data => {
            // Prefill the form with patient data
            document.getElementById('edit_patient_id').value = data.id;
            document.getElementById('edit_first_name').value = data.first_name;
            document.getElementById('edit_last_name').value = data.last_name;
            document.getElementById('edit_dob').value = data.birth_date;

            // Show the modal
            var editPatientModal = new bootstrap.Modal(document.getElementById('editPatientModal'));
            editPatientModal.show();
        });
}

document.getElementById('form_edit_patient').addEventListener('submit', function(event) {
    event.preventDefault();

    const patientId = document.getElementById('edit_patient_id').value;
    const firstName = document.getElementById('edit_first_name').value;
    const lastName = document.getElementById('edit_last_name').value;
    const dob = document.getElementById('edit_dob').value;

    const formData = new FormData();
    formData.append('patient_id', patientId);
    formData.append('first_name', firstName);
    formData.append('last_name', lastName);
    formData.append('dob', dob);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch('/edit_patient/', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload(); // Reload the page to see the changes
        } else {
            alert('Error updating patient');
        }
    });
});

function confirmDeletePatient(patientId) {
    if (confirm("Are you sure you want to delete this patient?")) {
        deletePatient(patientId);
    }
}

function deletePatient(patientId) {
    fetch(`/delete_patient/${patientId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload(); // Reload the page to see the changes
        } else {
            alert('Error deleting patient: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while trying to delete the patient.');
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