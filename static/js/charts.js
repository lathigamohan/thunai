// Finla - Chart.js Configuration with Black & Gold Theme

// Chart.js default configuration
Chart.defaults.color = '#f8f9fa';
Chart.defaults.borderColor = '#2d2d2d';
Chart.defaults.backgroundColor = 'rgba(255, 215, 0, 0.1)';
Chart.defaults.plugins.legend.labels.usePointStyle = true;

// Gold color palette
const goldPalette = {
    primary: '#FFD700',
    secondary: '#DAA520',
    accent: '#B8860B',
    dark: '#1a1a1a',
    light: '#f8f9fa',
    success: '#28a745',
    warning: '#ffc107',
    danger: '#dc3545',
    info: '#17a2b8'
};

// Chart color schemes
const colorSchemes = {
    gold: [goldPalette.primary, goldPalette.secondary, goldPalette.accent],
    mixed: [goldPalette.primary, goldPalette.success, goldPalette.warning, goldPalette.info, goldPalette.danger],
    gradient: ['#FFD700', '#FFA500', '#FF8C00', '#FF6347', '#FF4500']
};

// Global chart options
const defaultChartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            labels: {
                color: goldPalette.light,
                font: {
                    family: 'Inter, sans-serif',
                    size: 12
                }
            }
        },
        tooltip: {
            backgroundColor: goldPalette.dark,
            titleColor: goldPalette.primary,
            bodyColor: goldPalette.light,
            borderColor: goldPalette.primary,
            borderWidth: 1,
            cornerRadius: 8,
            displayColors: true
        }
    },
    scales: {
        x: {
            ticks: {
                color: goldPalette.light
            },
            grid: {
                color: 'rgba(255, 215, 0, 0.1)'
            }
        },
        y: {
            ticks: {
                color: goldPalette.light,
                callback: function(value) {
                    return '₹' + value.toLocaleString('en-IN');
                }
            },
            grid: {
                color: 'rgba(255, 215, 0, 0.1)'
            }
        }
    }
};

// Initialize home page charts
function initializeHomeCharts() {
    loadChartData().then(data => {
        if (data) {
            createWeeklyChart(data);
            createCategoryChart(data);
        }
    }).catch(error => {
        console.error('Error loading chart data:', error);
        showChartError();
    });
}

// Initialize analytics page charts
function initializeAnalyticsCharts() {
    loadChartData().then(data => {
        if (data) {
            createMonthlyTrendChart(data);
            createCategoryPieChart(data);
            createDailyPatternChart(data);
            createPaymentMethodChart(data);
            createWeeklyComparisonChart(data);
        }
    }).catch(error => {
        console.error('Error loading analytics data:', error);
        showChartError();
    });
}

// Load chart data from API
async function loadChartData() {
    try {
        const response = await fetch('/api/chart_data');
        if (!response.ok) {
            throw new Error('Failed to load chart data');
        }
        return await response.json();
    } catch (error) {
        console.error('Chart data loading error:', error);
        return null;
    }
}

// Weekly spending chart (Home page)
function createWeeklyChart(data) {
    const ctx = document.getElementById('weeklyChart');
    if (!ctx) return;

    const weeklyData = processWeeklyData(data.daily || {});
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: weeklyData.labels,
            datasets: [{
                label: 'Daily Spending',
                data: weeklyData.amounts,
                backgroundColor: goldPalette.primary,
                borderColor: goldPalette.secondary,
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            ...defaultChartOptions,
            plugins: {
                ...defaultChartOptions.plugins,
                title: {
                    display: true,
                    text: 'Last 7 Days Spending',
                    color: goldPalette.primary,
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            }
        }
    });
}

// Category breakdown chart (Home page)
function createCategoryChart(data) {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;

    const categories = data.categories || {};
    const categoryData = Object.entries(categories)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 5); // Top 5 categories

    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: categoryData.map(([category]) => capitalize(category)),
            datasets: [{
                data: categoryData.map(([, amount]) => amount),
                backgroundColor: colorSchemes.mixed,
                borderColor: goldPalette.dark,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: goldPalette.light,
                        font: {
                            size: 11
                        },
                        padding: 15
                    }
                },
                tooltip: {
                    backgroundColor: goldPalette.dark,
                    titleColor: goldPalette.primary,
                    bodyColor: goldPalette.light,
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${context.label}: ₹${value.toLocaleString('en-IN')} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Monthly trend chart (Analytics page)
function createMonthlyTrendChart(data) {
    const ctx = document.getElementById('monthlyTrendChart');
    if (!ctx) return;

    const monthlyData = processMonthlyData(data.daily || {});
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: monthlyData.labels,
            datasets: [{
                label: 'Monthly Spending',
                data: monthlyData.amounts,
                borderColor: goldPalette.primary,
                backgroundColor: 'rgba(255, 215, 0, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: goldPalette.primary,
                pointBorderColor: goldPalette.secondary,
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        },
        options: {
            ...defaultChartOptions,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                ...defaultChartOptions.plugins,
                title: {
                    display: true,
                    text: 'Spending Trend Over Time',
                    color: goldPalette.primary,
                    font: {
                        size: 16,
                        weight: 'bold'
                    }
                }
            }
        }
    });
}

// Category pie chart (Analytics page)
function createCategoryPieChart(data) {
    const ctx = document.getElementById('categoryPieChart');
    if (!ctx) return;

    const categories = data.categories || {};
    const categoryData = Object.entries(categories);

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: categoryData.map(([category]) => capitalize(category)),
            datasets: [{
                data: categoryData.map(([, amount]) => amount),
                backgroundColor: generateColorPalette(categoryData.length),
                borderColor: goldPalette.dark,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: goldPalette.light,
                        font: {
                            size: 12
                        },
                        padding: 15,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: goldPalette.dark,
                    titleColor: goldPalette.primary,
                    bodyColor: goldPalette.light,
                    callbacks: {
                        label: function(context) {
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${context.label}: ₹${value.toLocaleString('en-IN')} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Daily pattern chart (Analytics page)
function createDailyPatternChart(data) {
    const ctx = document.getElementById('dailyPatternChart');
    if (!ctx) return;

    const dailyPattern = processDailyPattern(data.daily || {});
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Average Spending',
                data: dailyPattern,
                backgroundColor: colorSchemes.gradient,
                borderColor: goldPalette.secondary,
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            ...defaultChartOptions,
            plugins: {
                ...defaultChartOptions.plugins,
                title: {
                    display: true,
                    text: 'Spending Pattern by Day of Week',
                    color: goldPalette.primary,
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            }
        }
    });
}

// Payment method chart (Analytics page)
function createPaymentMethodChart(data) {
    const ctx = document.getElementById('paymentMethodChart');
    if (!ctx) return;

    // This would need payment method data from backend
    const paymentMethods = {
        'GPay': 2500,
        'Cash': 800,
        'PhonePe': 1200,
        'Bank Transfer': 1500,
        'Credit Card': 900
    };

    new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: Object.keys(paymentMethods),
            datasets: [{
                label: 'Amount Spent',
                data: Object.values(paymentMethods),
                backgroundColor: colorSchemes.mixed,
                borderColor: goldPalette.dark,
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: goldPalette.dark,
                    titleColor: goldPalette.primary,
                    bodyColor: goldPalette.light,
                    callbacks: {
                        label: function(context) {
                            return `${context.label}: ₹${context.parsed.x.toLocaleString('en-IN')}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        color: goldPalette.light,
                        callback: function(value) {
                            return '₹' + value.toLocaleString('en-IN');
                        }
                    },
                    grid: {
                        color: 'rgba(255, 215, 0, 0.1)'
                    }
                },
                y: {
                    ticks: {
                        color: goldPalette.light
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Weekly comparison chart (Analytics page)
function createWeeklyComparisonChart(data) {
    const ctx = document.getElementById('weeklyComparisonChart');
    if (!ctx) return;

    const weeklyComparison = processWeeklyComparison(data.daily || {});
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: weeklyComparison.labels,
            datasets: [{
                label: 'This Week',
                data: weeklyComparison.thisWeek,
                backgroundColor: goldPalette.primary,
                borderColor: goldPalette.secondary,
                borderWidth: 1
            }, {
                label: 'Last Week',
                data: weeklyComparison.lastWeek,
                backgroundColor: 'rgba(255, 215, 0, 0.3)',
                borderColor: goldPalette.accent,
                borderWidth: 1
            }]
        },
        options: {
            ...defaultChartOptions,
            plugins: {
                ...defaultChartOptions.plugins,
                title: {
                    display: true,
                    text: 'Weekly Spending Comparison',
                    color: goldPalette.primary,
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                }
            }
        }
    });
}

// Data processing functions
function processWeeklyData(dailyData) {
    const today = new Date();
    const labels = [];
    const amounts = [];
    
    for (let i = 6; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const dateString = date.toISOString().split('T')[0];
        
        labels.push(date.toLocaleDateString('en-IN', { weekday: 'short' }));
        amounts.push(dailyData[dateString] || 0);
    }
    
    return { labels, amounts };
}

function processMonthlyData(dailyData) {
    const monthlyTotals = {};
    
    Object.entries(dailyData).forEach(([date, amount]) => {
        const monthYear = date.substring(0, 7); // YYYY-MM
        monthlyTotals[monthYear] = (monthlyTotals[monthYear] || 0) + amount;
    });
    
    const sortedMonths = Object.keys(monthlyTotals).sort();
    const labels = sortedMonths.map(month => {
        const [year, monthNum] = month.split('-');
        return new Date(year, monthNum - 1).toLocaleDateString('en-IN', { 
            year: 'numeric', 
            month: 'short' 
        });
    });
    
    return {
        labels,
        amounts: Object.values(monthlyTotals)
    };
}

function processDailyPattern(dailyData) {
    const dayTotals = new Array(7).fill(0);
    const dayCounts = new Array(7).fill(0);
    
    Object.entries(dailyData).forEach(([date, amount]) => {
        const dayOfWeek = new Date(date).getDay();
        const adjustedDay = dayOfWeek === 0 ? 6 : dayOfWeek - 1; // Monday = 0
        
        dayTotals[adjustedDay] += amount;
        dayCounts[adjustedDay]++;
    });
    
    return dayTotals.map((total, index) => 
        dayCounts[index] > 0 ? total / dayCounts[index] : 0
    );
}

function processWeeklyComparison(dailyData) {
    const today = new Date();
    const thisWeekData = [];
    const lastWeekData = [];
    const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    
    for (let i = 0; i < 7; i++) {
        // This week
        const thisWeekDate = new Date(today);
        thisWeekDate.setDate(today.getDate() - today.getDay() + i + 1);
        const thisWeekDateString = thisWeekDate.toISOString().split('T')[0];
        thisWeekData.push(dailyData[thisWeekDateString] || 0);
        
        // Last week
        const lastWeekDate = new Date(thisWeekDate);
        lastWeekDate.setDate(lastWeekDate.getDate() - 7);
        const lastWeekDateString = lastWeekDate.toISOString().split('T')[0];
        lastWeekData.push(dailyData[lastWeekDateString] || 0);
    }
    
    return { labels, thisWeek: thisWeekData, lastWeek: lastWeekData };
}

// Utility functions
function capitalize(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function generateColorPalette(count) {
    const colors = [...colorSchemes.mixed];
    while (colors.length < count) {
        colors.push(...colorSchemes.gradient);
    }
    return colors.slice(0, count);
}

function showChartError() {
    const errorMessage = `
        <div class="text-center p-4">
            <i class="fas fa-chart-bar text-muted fs-1 mb-3"></i>
            <p class="text-muted">Unable to load chart data</p>
            <button class="btn btn-outline-warning btn-sm" onclick="location.reload()">
                <i class="fas fa-refresh me-1"></i>Retry
            </button>
        </div>
    `;
    
    const chartContainers = document.querySelectorAll('canvas');
    chartContainers.forEach(canvas => {
        canvas.parentElement.innerHTML = errorMessage;
    });
}

// Export for global use
window.FinlaCharts = {
    initializeHomeCharts,
    initializeAnalyticsCharts,
    loadChartData,
    goldPalette,
    colorSchemes
};

console.log('📊 Finla Charts Module Loaded');
