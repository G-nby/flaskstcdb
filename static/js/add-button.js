document.addEventListener('DOMContentLoaded', function() {
    var container = document.getElementById('container');
    var form = document.getElementById('myForm');
    var addButton = document.getElementById('add-button');
    var removeButton = document.getElementById('remove-button');
    var elseButton = document.getElementById(('else-button'))
    var newCounter = 1;

    elseButton.addEventListener('click', function() {
        event.preventDefault();

        var newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.classList.add('form-control');
        newInput.classList.add('mb-3');
        newInput.setAttribute('name', 'new')
        newInput.setAttribute('placeholder', 'Input the pathway you want to align with the first pathway.')
        newCounter++;

        container.insertBefore(newInput, addButton);
        removeButton.style.display = 'inline';
        addButton.style.display = 'inline';
        elseButton.style.display = 'none';


    });

    addButton.addEventListener('click', function() {
        event.preventDefault();

        var newInput = document.createElement('input');
        newInput.type = 'text';
        newInput.classList.add('form-control');
        newInput.classList.add('mb-3');
        newInput.setAttribute('name', 'new')
        newInput.setAttribute('placeholder', 'Input the pathway you want to align with the first pathway.')
        newCounter++;

        container.insertBefore(newInput, addButton);
        removeButton.style.display = 'inline';
    });

    removeButton.addEventListener('click', function() {
        event.preventDefault();

        var inputFields = document.querySelectorAll('.form-control');
        if (inputFields.length > 1) {
            container.removeChild(inputFields[inputFields.length - 1]);
        }

        if (inputFields.length === 2) {
            removeButton.style.display = 'none';
            addButton.style.display = 'none';
            elseButton.style.display = 'inline';
        }
    });


});

