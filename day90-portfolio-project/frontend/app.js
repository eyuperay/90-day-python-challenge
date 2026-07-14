// Frontend JavaScript for Portfolio Project

const API_URL = 'http://localhost:8000';

// ==================== FETCH DATA ====================

async function fetchProjects() {
    try {
        const response = await fetch(`${API_URL}/projects`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching projects:', error);
        return [];
    }
}

async function fetchSkills() {
    try {
        const response = await fetch(`${API_URL}/skills`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching skills:', error);
        return [];
    }
}

async function fetchExperiences() {
    try {
        const response = await fetch(`${API_URL}/experiences`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching experiences:', error);
        return [];
    }
}

async function fetchStats() {
    try {
        const response = await fetch(`${API_URL}/stats`);
        return await response.json();
    } catch (error) {
        console.error('Error fetching stats:', error);
        return {};
    }
}

// ==================== RENDER FUNCTIONS ====================

function renderProjects(projects) {
    const container = document.getElementById('projects-container');
    if (!container) return;

    if (projects.length === 0) {
        container.innerHTML = '<p>No projects yet. Add some!</p>';
        return;
    }

    container.innerHTML = projects.map(project => `
        <div class="project-card">
            <h3>${project.title}</h3>
            <p>${project.description || 'No description'}</p>
            ${project.tech_stack ? `<div>${project.tech_stack.split(',').map(tech => 
                `<span class="tech">${tech.trim()}</span>`
            ).join('')}</div>` : ''}
            <div style="margin-top: 10px;">
                ${project.github_url ? `<a href="${project.github_url}" target="_blank">GitHub</a> ` : ''}
                ${project.live_url ? `<a href="${project.live_url}" target="_blank">Live Demo</a>` : ''}
            </div>
        </div>
    `).join('');
}

function renderSkills(skills) {
    const container = document.getElementById('skills-container');
    if (!container) return;

    if (skills.length === 0) {
        container.innerHTML = '<p>No skills yet. Add some!</p>';
        return;
    }

    container.innerHTML = skills.map(skill => `
        <div class="skill-item">
            <strong>${skill.name}</strong>
            ${skill.category ? `<div>${skill.category}</div>` : ''}
            <span class="level">${'★'.repeat(skill.level || 3)}</span>
        </div>
    `).join('');
}

function renderExperiences(experiences) {
    const container = document.getElementById('experience-container');
    if (!container) return;

    if (experiences.length === 0) {
        container.innerHTML = '<p>No experiences yet. Add some!</p>';
        return;
    }

    container.innerHTML = experiences.map(exp => `
        <div class="experience-item">
            <h3>${exp.position}</h3>
            <div class="company">${exp.company}</div>
            <div class="date">${exp.start_date || ''} - ${exp.is_current ? 'Present' : exp.end_date || ''}</div>
            <p>${exp.description || ''}</p>
        </div>
    `).join('');
}

function renderStats(stats) {
    document.getElementById('project-count').textContent = stats.total_projects || 0;
    document.getElementById('skill-count').textContent = stats.total_skills || 0;
    document.getElementById('experience-count').textContent = stats.total_experiences || 0;
}

// ==================== INITIALIZE ====================

async function init() {
    try {
        // Fetch all data
        const [projects, skills, experiences, stats] = await Promise.all([
            fetchProjects(),
            fetchSkills(),
            fetchExperiences(),
            fetchStats()
        ]);

        // Render
        renderProjects(projects);
        renderSkills(skills);
        renderExperiences(experiences);
        renderStats(stats);

        console.log('Portfolio loaded successfully!');
    } catch (error) {
        console.error('Error initializing portfolio:', error);
    }
}

// ==================== SAMPLE DATA (if API not available) ====================

function loadSampleData() {
    const sampleProjects = [
        {
            title: 'Web Scraping Tool',
            description: 'A Python tool for scraping real estate data',
            tech_stack: 'Python, BeautifulSoup, Requests'
        },
        {
            title: 'Data Visualization Dashboard',
            description: 'Interactive dashboard with Plotly',
            tech_stack: 'Python, Pandas, Plotly'
        },
        {
            title: 'REST API with FastAPI',
            description: 'Complete CRUD API with FastAPI',
            tech_stack: 'Python, FastAPI, SQLAlchemy'
        }
    ];

    const sampleSkills = [
        { name: 'Python', level: 5 },
        { name: 'FastAPI', level: 4 },
        { name: 'Docker', level: 3 },
        { name: 'SQL', level: 3 },
        { name: 'JavaScript', level: 2 }
    ];

    const sampleExperiences = [
        {
            company: 'Tech Corp',
            position: 'Software Developer',
            start_date: '2024-01',
            is_current: true,
            description: 'Developing Python applications'
        }
    ];

    renderProjects(sampleProjects);
    renderSkills(sampleSkills);
    renderExperiences(sampleExperiences);
    renderStats({ total_projects: 3, total_skills: 5, total_experiences: 1 });
}

// Start the app
document.addEventListener('DOMContentLoaded', () => {
    // Try to load from API, fallback to sample data
    init().catch(() => {
        console.log('Using sample data');
        loadSampleData();
    });
});
