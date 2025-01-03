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
