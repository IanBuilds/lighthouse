

//creates an unordered list of all the contents of a directory and its sub directories
document.getElementById("filepicker").addEventListener(
    "change",
    (event) => {
      let output = document.getElementById("listing");
      for (const file of event.target.files) {
        let item = document.createElement("li");
        item.className = "search"
        item.textContent = file.webkitRelativePath;
        output.appendChild(item);
      }
    },
    false
  );


  //searches to see if user input is in any of our results
function searchFiles() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('search');
      
    for (i = 0; i < x.length; i++) { 
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="list-item";                 
        }
    }
    
}

