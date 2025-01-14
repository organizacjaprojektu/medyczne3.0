function confirmDeleteReservation(reservationId) {
    if (confirm("Are you sure you want to delete this reservation?")) {
        fetch(`/delete_reservation/${reservationId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(data.message);
                    location.reload();
                } else {
                    alert(data.error);
                }
            });
    }
}


document.addEventListener('DOMContentLoaded', () => {
    const rows = document.querySelectorAll('.clickable-row');

    rows.forEach(row => {
        row.addEventListener('click', () => {
            const reservationId = row.getAttribute('data-reservation-id');

            fetch(`/reservation_details/${reservationId}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('modal-patient').textContent = `${data.patient.first_name} ${data.patient.last_name}`;
                    document.getElementById('modal-room').textContent = `${data.room.name} (${data.room.room_number})`;
                    document.getElementById('modal-start-date').textContent = data.start_date;
                    document.getElementById('modal-end-date').textContent = data.end_date;
                    document.getElementById('modal-description').textContent = data.description || 'No description provided';
                })
                .catch(error => console.error('Error fetching reservation details:', error));
        });
    });
});


function openEditReservationForm(reservationId) {
    fetch(`/get_reservation/${reservationId}/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch reservation data');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                // Wypełnienie modala danymi
                document.getElementById('edit_reservation_id').value = data.id;
                document.getElementById('edit_patient').value = data.patient_id;
                document.getElementById('edit_room').value = data.room_id;
                document.getElementById('edit_start_date').value = data.start_date;
                document.getElementById('edit_end_date').value = data.end_date;
                document.getElementById('edit_description').value = data.description;

                // Otwórz modal
                const editModal = new bootstrap.Modal(document.getElementById('editReservationModal'));
                editModal.show();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to load reservation data.');
        });
}

   document.getElementById('form_edit_reservation').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/edit_reservation/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to submit form');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.error || 'An error occurred.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update reservation.');
    });
});


