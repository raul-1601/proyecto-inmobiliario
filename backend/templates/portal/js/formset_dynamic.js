function setupFormset(prefix, addButtonId, formsContainerId) {
    const addButton = document.getElementById(addButtonId);
    const formsContainer = document.getElementById(formsContainerId);
    const totalFormsInput = document.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
    const maxFormsInput = document.querySelector(`input[name="${prefix}-MAX_NUM_FORMS"]`);

    addButton.addEventListener('click', function() {
        let totalForms = parseInt(totalFormsInput.value);
        const maxForms = parseInt(maxFormsInput.value);

        if (totalForms >= maxForms) {
            alert(`No puedes agregar más de ${maxForms} elementos.`);
            return;
        }

        // Clonar el primer formulario como plantilla
        const template = formsContainer.querySelector('.formset-form').cloneNode(true);

        // Limpiar valores
        template.querySelectorAll('input[type="file"], input[type="text"], textarea, select').forEach(input => {
            input.value = '';
        });

        // Resetear checkbox de DELETE si existe
        template.querySelectorAll('input[type="checkbox"]').forEach(input => {
            input.checked = false;
        });

        // Actualizar índices
        template.querySelectorAll('input, select, textarea').forEach(input => {
            if (input.name) input.name = input.name.replace(/-\d+-/, `-${totalForms}-`);
            if (input.id) input.id = input.id.replace(/-\d+-/, `-${totalForms}-`);
        });

        formsContainer.appendChild(template);

        totalFormsInput.value = totalForms + 1;
    });
}

document.addEventListener('DOMContentLoaded', function() {
    setupFormset('imagenes', 'add-imagen', 'imagenes-forms');
    setupFormset('documentos', 'add-documento', 'documentos-forms');
});
