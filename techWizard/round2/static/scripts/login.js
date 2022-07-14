

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
         $.ajax({
             type: "GET",
    url: "/LockSVB",
    data: {"EmployeeNumber":employeeid},
    contentType: 'application/json',
    processData: true,
    success: function(data){
var lock;  
lock = data.LockStatus;

var id;
id = data.EmployeeID;
 /*alert(lock);*/
 /* if (data["ServResponse"\ === "1")*/
  if(lock === "0")
  {
             var retVal = confirm("SVB is locked by employee id:  " + id + " .Do you want to override ?");
	     
               if(retVal==false)
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

},
             error:function(data) {
                 alert("NOT WORKING");
    }
      
      
         });
}

    
}
$(function() {
$(".svb-soc-name").load("svb_soc_name.txt");
$("#LOGIN").click(function(){
    var employeeid = document.getElementById("empid").value;
    var EmployeeDetails={ "EmployeeNumber":employeeid }; 
    
     $.ajax({
              type: "POST",
               url: "/LoginwithoutLock",
         data: JSON.stringify(EmployeeDetails),
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
                   alert("SVB is locked by "+ data.EmployeeID);
               }
          }
      });
    
	});
$("#LOG").click(function(){       
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
            $.ajax({
    url: "/LockSVB",
    data: {"EmployeeNumber":employeeid},
    contentType: 'application/json',
    processData: true,
    success: function(data){
var lock;  
lock = data.LockStatus;

var id;
id = data.EmployeeID;
 /*alert(lock);*/
 /* if (data["ServResponse"\ === "1")*/
  if(lock === "0")
  {
      
  var dialog = document.getElementById('OverRideMessage');
  dialog.style.top = ((window.innerHeight/2) - (dialog.offsetHeight/2))+'px';
  dialog.style.left = ((window.innerWidth/2) - (dialog.offsetWidth/2))+'px';
//  dialog.show();
      var retVal = confirm("SVB is locked by employee id:  " + id + " .Do you want to override ?");
      
      
      if(retVal==false)
               {
//                  form.preventDefault;
                  return false;
               }
//      $("#OverRideMessage").attr("someDialog", "dialog-confirm_ok-button");
//       document.getElementById('Close').onclick = function() {    
//        dialog.close();    
//    }; 
//    document.getElementById('OverRide').onclick = function() 
      else{  
               
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
  window.open("/registers.html","_self");
  return true;
 }
 }
});
//          dialog.close(); 
               }
    };
          
  }
 else
{
window.open("/registers.html","_self");
 return true;
}

},
                error:function(data) {
                    alert("NOT WOKRIGN")
                }
            });
}
     
});
});



