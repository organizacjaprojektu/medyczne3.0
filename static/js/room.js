function openEditRoomForm(roomId) {
    fetch(`/get_room/${roomId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('edit_room_id').value = data.id;
            document.getElementById('edit_room_number').value = data.room_number;
            document.getElementById('edit_type').value = data.type;
            document.getElementById('edit_description').value = data.description;

            var editRoomModal = new bootstrap.Modal(document.getElementById('editRoomModal'));
            editRoomModal.show();
        });
}

document.getElementById('form_edit_room').addEventListener('submit', function(event) {
    event.preventDefault();

    const roomId = document.getElementById('edit_room_id').value;
    const roomNumber = document.getElementById('edit_room_number').value;
    const type = document.getElementById('edit_type').value;
    const description = document.getElementById('edit_description').value;

    const formData = new FormData();
    formData.append('room_id', roomId);
    formData.append('room_number', roomNumber);
    formData.append('type', type);
    formData.append('description', description);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));

    fetch(`/edit_room/${roomId}/`, {
        method: 'POST',
        body: formData
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('Error updating room');
        }
    });
});

function confirmDeleteRoom(roomId) {
    if (confirm("Are you sure you want to delete this room?")) {
        deleteRoom(roomId);
    }
}

function deleteRoom(roomId) {
    fetch(`/delete_room/${roomId}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload()
        } else {
            alert('Error deleting room: ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while trying to delete the room.');
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
