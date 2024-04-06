document.addEventListener('DOMContentLoaded', function () {
    const monthNames = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ];
    
    // Get the elements where we will inject the month/year and the calendar days.
    const calendarMonthYear = document.getElementById('calendarMonthYear');
    const calendarDays = document.getElementById('calendarDays');

    function renderCalendar() {
        const today = new Date();
        const currentMonth = today.getMonth();
        const currentYear = today.getFullYear();

        // Total number of days in the current month.
        const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

        // The current day. Used to highlight the cell.
        const currentDay = today.getDate();

        // Day of the week the first day of the current month is.
        // 0: Sunday, 1: Monday, ..., 6: Saturday.
        const firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();

        // Set the month and year title.
        calendarMonthYear.textContent = `${monthNames[currentMonth]} ${currentYear}`;

        // Clear any existing cells.
        calendarDays.innerHTML = '';

        let date = 1; // Start at the first day of the month.

        // Create the rows for the calendar.
        for (let i = 0; i < 6; i++) {
            let row = document.createElement("tr");

            // Create each day cell.
            for (let j = 0; j < 7; j++) {
                if (i === 0 && j < firstDayOfMonth) {
                    // If this is the first row, we may need to add empty cells before the first day of the month starts.
                    row.appendChild(document.createElement("td"));
                } else if (date > daysInMonth) {
                    // If we've reached the end of the month, stop.
                    break;
                } else {
                    let cell = document.createElement("td");
                    cell.textContent = date;

                    // Highlight the current day.
                    if (date === currentDay) {
                        cell.classList.add("current-day");
                    }
                    
                    row.appendChild(cell);
                    date++;
                }
            }

            calendarDays.appendChild(row);

            // If we've reached the end of the month, we don't need to keep making rows.
            if (date > daysInMonth) {
                break;
            }
        }
    }

    renderCalendar();


});