// Search Feature
$(document).ready(function() {
 $(".search").keyup(function () {
   var searchTerm = $(".search").val();
   var listItem = $('.results tbody').children('tr');
   var searchSplit = searchTerm.replace(/ /g, "'):containsi('")

 $.extend($.expr[':'], {'containsi': function(elem, i, match, array){
       return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
   }
 });

 $(".results tbody tr").not(":containsi('" + searchSplit + "')").each(function(e){
   $(this).attr('visible','false');
 });

 $(".results tbody tr:containsi('" + searchSplit + "')").each(function(e){
   $(this).attr('visible','true');
 });

 var jobCount = $('.results tbody tr[visible="true"]').length;
   $('.counter').text(jobCount + ' item');

 if(jobCount == '0') {$('.no-result').show();}
   else {$('.no-result').hide();}
          });
});
//
// $(document).ready(function() {
//   $(".search").keyup(function () {
//     var searchTerm = $(".search").val();
//     var listItem = $('.results tbody').children('tr');
//     var searchSplit = searchTerm.replace(/ /g, "'):containsi('")
//
//   $.extend($.expr[':'], {'containsi': function(elem, i, match, array){
//         return (elem.textContent || elem.innerText || '').toLowerCase().indexOf((match[3] || "").toLowerCase()) >= 0;
//     }
//   });
//
//   $(".results tbody tr").each(function(e){
//     if (!":containsi('" + searchSplit + "')" ){
//       $(this).attr('visible','false');
//     }
//     else{
//        $(this).attr('visible','true');
//     }
//   });
//
//   var jobCount = $('.results tbody tr[visible="true"]').length;
//     $('.counter').text(jobCount + ' item');
//
//   if(jobCount == '0') {$('.no-result').show();}
//     else {$('.no-result').hide();}
// 		  });
// });

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



