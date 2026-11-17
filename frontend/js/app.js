
const addJobButton = document.querySelector("#add-job-btn");
const cancelJobButton = document.querySelector("#cancel-job-btn");
const jobDialog = document.querySelector("#job-dialog");
const jobForm = document.querySelector("#job-form");

const API_URL = `${window.location.origin}/jobs`;

let jobs = [];

let editingJobId = null;

const searchInput = document.querySelector("#job-search");
const statusFilter = document.querySelector("#status-filter");

searchInput.addEventListener("input", renderJobs);
statusFilter.addEventListener("change", renderJobs);

addJobButton.addEventListener("click", function() {
    editingJobId = null;

    jobForm.reset();

    jobDialog.querySelector("h2").textContent = "Add Job Application";
    jobForm.querySelector('button[type="submit"]').textContent = "Save Application";

    jobDialog.showModal();
});

cancelJobButton.addEventListener("click", function() {
    jobDialog.close();
});



jobForm.addEventListener("submit", async function(event) {
    event.preventDefault();
    const submitButton = jobForm.querySelector('button[type="submit"]');

    if (submitButton.disabled) return;

    submitButton.disabled = true;

    const formData = new FormData(jobForm);

    const jobData = {
        company: formData.get("company"),
        position: formData.get("position"),
        status: formData.get("status"),
        appliedDate: formData.get("appliedDate")
    };

    const isEditing = editingJobId !== null;

    const url = isEditing
        ? `${API_URL}/${editingJobId}`
        : API_URL;

    const method = isEditing ? "PATCH" : "POST";

    try {
        const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jobData)
        });

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        const loaded = await loadJobs();

        if (!loaded) {
            return;
        }

        editingJobId = null;
        jobForm.reset();
        jobDialog.close();

    } catch (error) {
        console.error("Failed to save job:", error);
        alert("Could not save the application.");
    }
    finally {
        submitButton.disabled = false;
    }
});

function renderJobs() {
    const jobList = document.querySelector("#job-list");

    jobList.replaceChildren();

    if (jobs.length === 0) {
        const message = document.createElement("p");
        message.className = "empty-message";
        message.textContent = "No applications yet.";
        jobList.appendChild(message);
        return;
    }

    const searchTerm = searchInput.value.trim().toLowerCase();
    const selectedStatus = statusFilter.value;

    const filteredJobs = jobs.filter(function(job) {
        const matchesSearch =
            job.company.toLowerCase().includes(searchTerm) ||
            job.position.toLowerCase().includes(searchTerm);

        const matchesStatus =
            selectedStatus === "All" ||
            job.status === selectedStatus;

        return matchesSearch && matchesStatus;
    });

    if (filteredJobs.length === 0) {
        const message = document.createElement("p");
        message.className = "empty-message";
        message.textContent = "No matching applications found.";

        jobList.appendChild(message);
        return;
    }

    filteredJobs.forEach(function(job) {
        const jobCard = document.createElement("div");
        jobCard.className = "job-item";

        const details = document.createElement("div");

        const company = document.createElement("h3");
        company.textContent = job.company;

        const position = document.createElement("p");
        position.textContent = job.position;

        const status = document.createElement("span");
        status.className = "job-status";
        status.textContent = job.status;

        details.append(company, position);

        const editButton = document.createElement("button");
        editButton.textContent = "Edit";
        editButton.className = "edit-btn";

        editButton.addEventListener("click", function() {
            editJob(job.id);
        });
        
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.className = "delete-btn";

        deleteButton.addEventListener("click", function() {
            deleteJob(job.id);
        });

        const actions = document.createElement("div");
        actions.className = "job-actions";
        actions.append(status, editButton, deleteButton);

        jobCard.append(details, actions);

        jobList.appendChild(jobCard);
    });
}


function editJob(id) {
    const job = jobs.find(function(job) {
        return job.id === id;
    });

    if (!job) {
        return;
    }

    editingJobId = id;

    jobForm.elements["company"].value = job.company;
    jobForm.elements["position"].value = job.position;
    jobForm.elements["status"].value = job.status;
    jobForm.elements["appliedDate"].value = job.appliedDate;

    jobDialog.querySelector("h2").textContent = "Edit Job Application";
    jobForm.querySelector('button[type="submit"]').textContent = "Save Changes";

    jobDialog.showModal();
}



async function deleteJob(id) {
    const confirmed = confirm("Delete this job application?");

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        await loadJobs();

    } catch (error) {
        console.error("Failed to delete job:", error);
        alert("Could not delete the application.");
    }
}

function updateStats() {
    const total = jobs.length;

    const interviews = jobs.filter(function(job) {
        return job.status === "Interview";
    }).length;

    const offers = jobs.filter(function(job) {
        return job.status === "Offer";
    }).length;

    document.querySelector("#total-count").textContent = total;
    document.querySelector("#interview-count").textContent = interviews;
    document.querySelector("#offer-count").textContent = offers;
}


async function loadJobs() {
    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }

        jobs = await response.json();

        renderJobs();
        updateStats();

        return true;
    } catch (error) {
        console.error("Failed to load jobs:", error);
        alert("Could not load applications. Check your connection.");

        return false;
    }
}

loadJobs();