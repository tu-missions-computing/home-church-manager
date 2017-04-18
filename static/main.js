$('#confirmModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var url = button.data('url') // Extract info from data-* attributes
    var firstname = button.data('firstname')
    var lastname = button.data('lastname')
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-body').text('Are you sure you want to remove ' +  firstname + ' ' + lastname + '?')
    modal.find('#modal-confirm').attr("href", url)
})