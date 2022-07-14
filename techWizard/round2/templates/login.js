

function validate(form){
/*alert("function in");*/

var employeeid = document.getElementById("empid").value;
/*alert(employeeid);*/
 if(employeeid === "")
 {
   $('#empty-alert').show();
         $("#empty-alert").fadeTo(4000, 500).slideUp(500, function(){
    $("#empty-alert").alert('hide');
 })
   return false;
}

else
{
$.post('/LockSVB',{"EmployeeNumber":employeeid}, function(data){
var lock;
lock = data.LockStatus;

var id;
id = data.EmployeeID;
 /*alert(lock);*/
 /* if (data["ServResponse"\ === "1")*/
  if(lock === "0")
  {
             var retVal = confirm("SVB is locked by employee id:  " + id + " .Do you want to override ?");

               if(!retVal)
               {
		  alert("Return false");
                  form.preventDefault;
                  return false;
               }
               else
               {
        var overrideDetailsobject={ "EmployeeNumber": employeeid };

           $.ajax({
              type: "POST",
               url: "/OverrideLockSVB",
              data: JSON.stringify(overrideDetailsobject),
             contentType: 'application/json',
             dataType: 'json',
          error: function(data) {
                 alert("error");
            },
           success: function(data) {
            //    $.post('/OverrideLockSVB',{"EmployeeNumber":employeeid},function(data){
  var user;
  user=data.LockStatus;
  if(user === "0")
  {
   alert("Could not override");
   return false;
 }
 else
 {

  return true;
 }
 }
});
               }
  }
 else
{
 return true;
}

});
}



}
$(function() {
$("#LOGIN").click(function(){
    var deleteDetailsobject={ "FileName": "ffdads" };
     $.ajax({
              type: "POST",
               url: "/LoginwithoutLock",
              data: JSON.stringify(deleteDetailsobject),
             contentType: 'application/json',
             dataType: 'json',
          error: function(data) {
                 alert("error");
            },
           success: function(data) {
               if(data["LockStatus"]==='1')
                   {
                       window.open("/registers.html","_self");
                   }
               else{
                   alert("Locked by other User");
               }

               //var json = $.parseJSON(data);

          }
      });

	});
$("#LOG").click(function(){
    alert("COMGUISDG HERE R     ");
    $(this).children('div.dialog-text').replaceWith("<h3><b>Users</b></h3>" + makeDialogTable(users) + "<h3><b>Owners</b></h3>" + makeDialogTable(owners));
    });
});
