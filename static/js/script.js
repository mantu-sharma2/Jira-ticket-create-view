/**
 * Jira Ticket Manager - Frontend JavaScript
 * Clean, well-structured code for handling file uploads and ticket management
 */

class JiraTicketManager {
  constructor() {
    this.currentPreviewId = null;
    this.currentOperationId = null;
    this.statusCheckInterval = null;

    // DOM elements
    this.elements = {};

    this.init();
  }

  /**
   * Initialize the application
   */
  init() {
    console.log("Initializing Jira Ticket Manager...");

    this.initializeElements();
    this.setupEventListeners();
    this.showSection("upload");

    console.log("Jira Ticket Manager initialized successfully");
  }

  /**
   * Initialize DOM elements
   */
  initializeElements() {
    // Upload elements
    this.elements.uploadArea = document.getElementById("uploadArea");
    this.elements.fileInput = document.getElementById("fileInput");

    // Section elements
    this.elements.parsingSection = document.getElementById("parsingSection");
    this.elements.previewSection = document.getElementById("previewSection");
    this.elements.progressSection = document.getElementById("progressSection");

    // Parsing elements
    this.elements.parsingMessage = document.getElementById("parsingMessage");

    // Preview elements
    this.elements.previewStats = document.getElementById("previewStats");
    this.elements.previewTable = document.getElementById("previewTable");
    this.elements.previewTableHeader =
      document.getElementById("previewTableHeader");
    this.elements.previewTableBody =
      document.getElementById("previewTableBody");

    // Progress elements
    this.elements.progressFill = document.getElementById("progressFill");
    this.elements.progressText = document.getElementById("progressText");
    this.elements.progressPercentage =
      document.getElementById("progressPercentage");
    this.elements.resultsList = document.getElementById("resultsList");

    // Button elements
    this.elements.resetBtn = document.getElementById("resetBtn");
    this.elements.createTicketsBtn =
      document.getElementById("createTicketsBtn");
    this.elements.newFileBtn = document.getElementById("newFileBtn");

    // View elements
    this.elements.ticketIdInput = document.getElementById("ticketIdInput");
    this.elements.searchBtn = document.getElementById("searchBtn");
    this.elements.ticketDetails = document.getElementById("ticketDetails");
    this.elements.errorMessage = document.getElementById("errorMessage");
    this.elements.errorText = document.getElementById("errorText");
  }

  /**
   * Setup event listeners
   */
  setupEventListeners() {
    // Tab functionality
    this.setupTabListeners();

    // File upload functionality
    this.setupFileUploadListeners();

    // Button functionality
    this.setupButtonListeners();

    // Search functionality
    this.setupSearchListeners();
  }

  /**
   * Setup tab navigation listeners
   */
  setupTabListeners() {
    document.querySelectorAll(".tab-btn").forEach((button) => {
      button.addEventListener("click", () => {
        const tabName = button.getAttribute("data-tab");
        this.switchTab(tabName);
      });
    });
  }

  /**
   * Setup file upload listeners
   */
  setupFileUploadListeners() {
    // Upload area click (but not on the file input)
    if (this.elements.uploadArea) {
      this.elements.uploadArea.addEventListener("click", (e) => {
        // Don't trigger if clicking on the file input
        if (e.target.closest(".styled-file-input")) {
          return;
        }
        e.preventDefault();
        e.stopPropagation();
        this.elements.fileInput.click();
      });

      // Drag and drop
      this.elements.uploadArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.elements.uploadArea.classList.add("dragover");
      });

      this.elements.uploadArea.addEventListener("dragleave", (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.elements.uploadArea.classList.remove("dragover");
      });

      this.elements.uploadArea.addEventListener("drop", (e) => {
        e.preventDefault();
        e.stopPropagation();
        this.elements.uploadArea.classList.remove("dragover");
        const files = e.dataTransfer.files;
        if (files.length > 0) {
          this.handleFileUpload(files[0]);
        }
      });
    }

    // File input change
    if (this.elements.fileInput) {
      this.elements.fileInput.addEventListener("change", (e) => {
        e.preventDefault();
        if (e.target.files.length > 0) {
          this.handleFileUpload(e.target.files[0]);
        }
      });
    }
  }

  /**
   * Setup button listeners
   */
  setupButtonListeners() {
    // Reset button
    if (this.elements.resetBtn) {
      this.elements.resetBtn.addEventListener("click", () => {
        this.resetUpload();
      });
    }

    // Create tickets button
    if (this.elements.createTicketsBtn) {
      this.elements.createTicketsBtn.addEventListener("click", () => {
        this.startTicketCreation();
      });
    }

    // New file button
    if (this.elements.newFileBtn) {
      this.elements.newFileBtn.addEventListener("click", () => {
        this.resetUpload();
      });
    }
  }

  /**
   * Setup search listeners
   */
  setupSearchListeners() {
    // Search button
    if (this.elements.searchBtn) {
      this.elements.searchBtn.addEventListener("click", () => {
        this.searchTicket();
      });
    }

    // Enter key in search input
    if (this.elements.ticketIdInput) {
      this.elements.ticketIdInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
          this.searchTicket();
        }
      });
    }
  }

  /**
   * Switch between tabs
   */
  switchTab(tabName) {
    // Update active tab button
    document.querySelectorAll(".tab-btn").forEach((btn) => {
      btn.classList.remove("active");
    });
    document.querySelector(`[data-tab="${tabName}"]`).classList.add("active");

    // Update active tab content
    document.querySelectorAll(".tab-content").forEach((content) => {
      content.classList.remove("active");
    });
    document.getElementById(`${tabName}-tab`).classList.add("active");
  }

  /**
   * Handle file upload
   */
  handleFileUpload(file) {
    console.log("Handling file upload:", file.name);

    // Validate file type
    if (!this.isValidFileType(file)) {
      this.showError("Please select a valid Excel file (.xlsx or .xls)");
      return;
    }

    // Show parsing section
    this.showSection("parsing");
    this.elements.parsingMessage.textContent = "Reading Excel file...";

    // Prepare form data
    const formData = new FormData();
    formData.append("file", file);

    // Upload file
    fetch("/api/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        console.log("Upload response status:", response.status);
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log("Upload response data:", data);
        if (data.success) {
          this.currentPreviewId = data.data.preview_id;
          this.elements.parsingMessage.textContent =
            "File parsed successfully!";

          // Show preview after delay
          setTimeout(() => {
            this.showPreview(data.data);
          }, 1000);
        } else {
          this.showError(data.error || "Upload failed");
          this.showSection("upload");
        }
      })
      .catch((error) => {
        console.error("Upload error:", error);
        this.showError("Error uploading file: " + error.message);
        this.showSection("upload");
      });
  }

  /**
   * Validate file type
   */
  isValidFileType(file) {
    return file.name.match(/\.(xlsx|xls)$/i);
  }

  /**
   * Show preview of uploaded data
   */
  showPreview(data) {
    console.log("=== SHOW PREVIEW START ===");
    console.log("Showing preview with data:", data);
    console.log("Data columns:", data.columns);
    console.log("Data rows:", data.data);
    console.log("Total rows:", data.total_rows);

    // Update preview stats - show first 5 rows info
    if (this.elements.previewStats) {
      const displayRows = Math.min(5, data.total_rows);
      this.elements.previewStats.textContent = `First ${displayRows} rows of ${data.total_rows} total, ${data.columns.length} columns`;
      console.log(
        "Updated preview stats:",
        this.elements.previewStats.textContent
      );
    } else {
      console.error("Preview stats element not found!");
    }

    // Populate table headers
    if (this.elements.previewTableHeader) {
      this.elements.previewTableHeader.innerHTML = "";
      data.columns.forEach((column) => {
        const th = document.createElement("th");
        th.textContent = column;
        this.elements.previewTableHeader.appendChild(th);
      });
      console.log("Populated table headers:", data.columns);
    } else {
      console.error("Preview table header element not found!");
    }

    // Populate table body - only first 5 rows
    if (this.elements.previewTableBody) {
      this.elements.previewTableBody.innerHTML = "";
      const rowsToShow = data.data.slice(0, 5); // Only show first 5 rows
      rowsToShow.forEach((row, index) => {
        const tr = document.createElement("tr");
        data.columns.forEach((column) => {
          const td = document.createElement("td");
          const value = row[column] || "";
          td.textContent = value;
          td.title = value;
          tr.appendChild(td);
        });
        this.elements.previewTableBody.appendChild(tr);
      });
      console.log(
        "Populated table body with",
        rowsToShow.length,
        "rows (first 5)"
      );
    } else {
      console.error("Preview table body element not found!");
    }

    console.log("About to show preview section");
    this.showSection("preview");
    console.log("Preview section should now be visible");

    // Additional verification
    setTimeout(() => {
      const previewSection = document.getElementById("previewSection");
      if (previewSection) {
        console.log(
          "Preview section display style:",
          previewSection.style.display
        );
        console.log(
          "Preview section visibility:",
          previewSection.style.visibility
        );
        console.log(
          "Preview section computed display:",
          window.getComputedStyle(previewSection).display
        );
      } else {
        console.error("Preview section not found in verification!");
      }
    }, 100);

    console.log("=== SHOW PREVIEW END ===");
  }

  /**
   * Start ticket creation process
   */
  startTicketCreation() {
    if (!this.currentPreviewId) {
      this.showError("No preview data available");
      return;
    }

    // Disable button and show loading state
    this.setButtonLoading(
      this.elements.createTicketsBtn,
      true,
      "Creating Tickets..."
    );

    // Show progress section
    this.showSection("progress");

    // Start ticket creation
    fetch("/api/create-tickets", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        preview_id: this.currentPreviewId,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          this.currentOperationId = data.data.operation_id;
          this.startStatusCheck();
        } else {
          this.showError(data.error || "Failed to start ticket creation");
          this.showSection("preview");
        }
      })
      .catch((error) => {
        this.showError("Error creating tickets: " + error.message);
        this.showSection("preview");
      })
      .finally(() => {
        this.setButtonLoading(
          this.elements.createTicketsBtn,
          false,
          "Create Tickets"
        );
      });
  }

  /**
   * Start status checking for ticket creation
   */
  startStatusCheck() {
    if (this.statusCheckInterval) {
      clearInterval(this.statusCheckInterval);
    }

    this.statusCheckInterval = setInterval(() => {
      fetch(`/api/status/${this.currentOperationId}`)
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            this.updateProgress(data.data);

            if (data.data.status === "completed") {
              clearInterval(this.statusCheckInterval);
              this.showFinalResults(data.data);
            }
          } else {
            console.error("Status check error:", data.error);
          }
        })
        .catch((error) => {
          console.error("Error checking status:", error);
        });
    }, 1000);
  }

  /**
   * Update progress display
   */
  updateProgress(data) {
    const total = data.total_tickets;
    const completed = data.completed + data.failed;
    const percentage = total > 0 ? Math.round((completed / total) * 100) : 0;

    this.elements.progressFill.style.width = `${percentage}%`;
    this.elements.progressText.textContent = `${completed} / ${total} completed`;
    this.elements.progressPercentage.textContent = `${percentage}%`;

    // Update results list
    this.elements.resultsList.innerHTML = "";
    data.results.forEach((result) => {
      const resultItem = this.createResultItem(result);
      this.elements.resultsList.appendChild(resultItem);
    });
  }

  /**
   * Create result item element
   */
  createResultItem(result) {
    const resultItem = document.createElement("div");
    resultItem.className = `result-item ${result.status}`;

    let statusIcon = "";
    let statusText = "";

    switch (result.status) {
      case "processing":
        statusIcon =
          '<i class="fas fa-spinner fa-spin result-status processing"></i>';
        statusText = "Processing...";
        break;
      case "completed":
        statusIcon =
          '<i class="fas fa-check-circle result-status success"></i>';
        statusText = result.result.success
          ? `Created: ${result.result.ticket_id}`
          : `Failed: ${result.result.error}`;
        break;
      case "failed":
        statusIcon = '<i class="fas fa-times-circle result-status failed"></i>';
        statusText = `Failed: ${result.result.error}`;
        break;
    }

    resultItem.innerHTML = `
            ${statusIcon}
            <div class="result-info">
                <div class="result-summary">Row ${result.row}: ${result.summary}</div>
                <div class="result-details">${statusText}</div>
            </div>
        `;

    return resultItem;
  }

  /**
   * Show final results
   */
  showFinalResults(data) {
    const successCount = data.completed;
    const failedCount = data.failed;
    const totalCount = data.total_tickets;

    const summaryDiv = document.createElement("div");
    summaryDiv.className = "result-summary-message";
    summaryDiv.innerHTML = `
            <h4>Ticket Creation Complete!</h4>
            <p>Successfully created: ${successCount} tickets</p>
            <p>Failed: ${failedCount} tickets</p>
            <p>Total processed: ${totalCount} tickets</p>
        `;

    this.elements.resultsList.insertBefore(
      summaryDiv,
      this.elements.resultsList.firstChild
    );
  }

  /**
   * Reset upload process
   */
  resetUpload() {
    this.showSection("upload");

    // Clear file input
    if (this.elements.fileInput) {
      this.elements.fileInput.value = "";
    }

    // Reset variables
    this.currentPreviewId = null;
    this.currentOperationId = null;

    // Clear intervals
    if (this.statusCheckInterval) {
      clearInterval(this.statusCheckInterval);
      this.statusCheckInterval = null;
    }

    // Clear preview data
    if (this.elements.previewTableHeader) {
      this.elements.previewTableHeader.innerHTML = "";
    }
    if (this.elements.previewTableBody) {
      this.elements.previewTableBody.innerHTML = "";
    }
    if (this.elements.previewStats) {
      this.elements.previewStats.textContent = "";
    }

    // Clear progress
    if (this.elements.progressFill) {
      this.elements.progressFill.style.width = "0%";
    }
    if (this.elements.progressText) {
      this.elements.progressText.textContent = "0 / 0 completed";
    }
    if (this.elements.progressPercentage) {
      this.elements.progressPercentage.textContent = "0%";
    }
    if (this.elements.resultsList) {
      this.elements.resultsList.innerHTML = "";
    }
  }

  /**
   * Show specific section
   */
  showSection(sectionName) {
    console.log("Showing section:", sectionName);

    // Hide all sections first
    const sections = [
      this.elements.parsingSection,
      this.elements.previewSection,
      this.elements.progressSection,
    ];

    sections.forEach((section) => {
      if (section) {
        console.log("Hiding section:", section.id);
        section.style.display = "none";
      }
    });

    // Hide upload area (which is the default view)
    if (this.elements.uploadArea) {
      console.log("Hiding upload area");
      this.elements.uploadArea.style.display = "none";
    }

    // Show selected section
    switch (sectionName) {
      case "upload":
        if (this.elements.uploadArea) {
          console.log("Showing upload area");
          this.elements.uploadArea.style.display = "block";
        }
        break;
      case "parsing":
        if (this.elements.parsingSection) {
          console.log("Showing parsing section");
          this.elements.parsingSection.style.display = "block";
        }
        break;
      case "preview":
        if (this.elements.previewSection) {
          console.log("Showing preview section");
          this.elements.previewSection.style.display = "block";
        } else {
          console.error("Preview section element not found!");
          // Fallback: try to find it directly
          const previewSection = document.getElementById("previewSection");
          if (previewSection) {
            console.log("Found preview section via direct ID lookup");
            previewSection.style.display = "block";
          } else {
            console.error("Preview section not found even with direct lookup!");
          }
        }
        break;
      case "progress":
        if (this.elements.progressSection) {
          console.log("Showing progress section");
          this.elements.progressSection.style.display = "block";
        }
        break;
    }
  }

  /**
   * Show error message
   */
  showError(message) {
    console.error("Showing error:", message);

    const errorDiv = document.createElement("div");
    errorDiv.className = "error-message";
    errorDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i>
            <span>${message}</span>
        `;

    const currentSection = document.querySelector(".tab-content.active");
    if (currentSection) {
      currentSection.appendChild(errorDiv);

      setTimeout(() => {
        if (errorDiv.parentElement) {
          errorDiv.remove();
        }
      }, 5000);
    }
  }

  /**
   * Set button loading state
   */
  setButtonLoading(button, loading, text) {
    if (!button) return;

    if (loading) {
      button.disabled = true;
      button.innerHTML = `<i class="fas fa-spinner fa-spin"></i> ${text}`;
    } else {
      button.disabled = false;
      button.innerHTML = `<i class="fas fa-rocket"></i> ${text}`;
    }
  }

  /**
   * Search for a ticket
   */
  searchTicket() {
    const ticketId = this.elements.ticketIdInput.value.trim();
    if (!ticketId) {
      this.showTicketError("Please enter a ticket ID");
      return;
    }

    // Show loading state
    this.setButtonLoading(this.elements.searchBtn, true, "Searching...");

    fetch(`/api/ticket/${ticketId}`)
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.displayTicketDetails(data.data);
        } else {
          this.showTicketError(data.error || "Ticket not found");
        }
      })
      .catch((error) => {
        this.showTicketError("Error searching ticket: " + error.message);
      })
      .finally(() => {
        this.setButtonLoading(this.elements.searchBtn, false, "Search");
      });
  }

  /**
   * Display ticket details
   */
  displayTicketDetails(ticket) {
    // Populate ticket information
    const elements = {
      ticketTitle: ticket.fields.summary,
      ticketKey: ticket.key,
      issueType: ticket.fields.issuetype.name,
      priority: ticket.fields.priority
        ? ticket.fields.priority.name
        : "Not set",
      assignee: ticket.fields.assignee
        ? ticket.fields.assignee.displayName
        : "Unassigned",
      created: new Date(ticket.fields.created).toLocaleDateString(),
      status: ticket.fields.status.name,
      labels: ticket.fields.labels
        ? ticket.fields.labels.join(", ")
        : "No labels",
    };

    Object.entries(elements).forEach(([id, value]) => {
      const element = document.getElementById(id);
      if (element) {
        element.textContent = value;
      }
    });

    // Handle description
    let description = "";
    if (ticket.fields.description) {
      if (typeof ticket.fields.description === "string") {
        description = ticket.fields.description;
      } else if (ticket.fields.description.content) {
        description = this.extractTextFromADF(
          ticket.fields.description.content
        );
      }
    }

    const descElement = document.getElementById("description");
    if (descElement) {
      descElement.textContent = description || "No description";
    }

    // Set Jira link
    const jiraLink = document.getElementById("jiraLink");
    if (jiraLink) {
      jiraLink.href = `${window.location.origin.replace("4000", "")}/browse/${
        ticket.key
      }`;
    }

    // Show ticket details
    if (this.elements.ticketDetails) {
      this.elements.ticketDetails.style.display = "block";
    }
  }

  /**
   * Extract text from Atlassian Document Format
   */
  extractTextFromADF(content) {
    let text = "";

    function extractFromNode(node) {
      if (node.type === "text") {
        text += node.text || "";
      } else if (node.content) {
        node.content.forEach(extractFromNode);
      }
    }

    if (Array.isArray(content)) {
      content.forEach(extractFromNode);
    } else {
      extractFromNode(content);
    }

    return text;
  }

  /**
   * Show ticket error
   */
  showTicketError(message) {
    if (this.elements.errorText) {
      this.elements.errorText.textContent = message;
    }
    if (this.elements.errorMessage) {
      this.elements.errorMessage.style.display = "flex";
    }
  }
}

// Initialize application when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  window.jiraManager = new JiraTicketManager();
});
