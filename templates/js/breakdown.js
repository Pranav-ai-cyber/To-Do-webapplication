// --- Task Breakdown (Gemini Feature) ---
async function handleBreakdownTask(task) {
    try {
        // Show modal and loading state
        dom.breakdownModal.classList.remove('opacity-0', 'pointer-events-none');
        dom.breakdownTaskTitle.textContent = task.title;
        dom.breakdownLoading.classList.remove('hidden');
        dom.breakdownError.classList.add('hidden');
        dom.suggestedSubtasks.innerHTML = '';
        
        // Call the API
        const response = await fetch('/api/tasks/breakdown', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: task.title,
                description: task.description
            }),
        });

        if (!response.ok) {
            throw new Error('Failed to generate subtasks');
        }

        const data = await response.json();
        
        // Hide loading state
        dom.breakdownLoading.classList.add('hidden');
        
        // Update subtask count
        dom.subtaskCount.textContent = `${data.subtasks.length} subtasks suggested`;
        
        // Clear previous subtasks
        dom.suggestedSubtasks.innerHTML = '';
        
        // Add new subtasks
        data.subtasks.forEach(subtaskTitle => {
            const subtaskElement = dom.subtaskTemplate.content.cloneNode(true);
            const titleInput = subtaskElement.querySelector('.subtask-title');
            const toggleBtn = subtaskElement.querySelector('.subtask-toggle-btn');
            
            titleInput.value = subtaskTitle;
            toggleBtn.textContent = 'Add';
            
            toggleBtn.addEventListener('click', async () => {
                await addSubtask(subtaskTitle);
                toggleBtn.textContent = 'Added';
                toggleBtn.disabled = true;
                toggleBtn.classList.add('opacity-50');
            });
            
            dom.suggestedSubtasks.appendChild(subtaskElement);
        });
        
    } catch (error) {
        console.error('Error in task breakdown:', error);
        dom.breakdownLoading.classList.add('hidden');
        dom.breakdownError.classList.remove('hidden');
        dom.breakdownErrorMessage.textContent = error.message;
    }
}

async function handleAddAllSubtasks() {
    try {
        const subtaskElements = dom.suggestedSubtasks.querySelectorAll('.subtask-item');
        const subtaskPromises = Array.from(subtaskElements).map(element => {
            const titleInput = element.querySelector('.subtask-title');
            const toggleBtn = element.querySelector('.subtask-toggle-btn');
            
            if (!toggleBtn.disabled) {
                toggleBtn.textContent = 'Added';
                toggleBtn.disabled = true;
                toggleBtn.classList.add('opacity-50');
                return addSubtask(titleInput.value);
            }
            return Promise.resolve();
        });
        
        await Promise.all(subtaskPromises);
        showToast('All subtasks added successfully!', 'success');
        closeBreakdownModal();
        
    } catch (error) {
        console.error('Error adding all subtasks:', error);
        showToast('Failed to add all subtasks', 'error');
    }
}

function closeBreakdownModal() {
    dom.breakdownModal.classList.add('opacity-0', 'pointer-events-none');
    // Reset state
    dom.breakdownTaskTitle.textContent = '';
    dom.suggestedSubtasks.innerHTML = '';
    dom.subtaskCount.textContent = '0 subtasks suggested';
    dom.breakdownError.classList.add('hidden');
}