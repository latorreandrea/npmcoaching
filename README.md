# npmcoaching
first prototype

## Table of Contents

- [UX](#ux)
  - [Strategy](#strategy)
    - [Project goal: Empower Personal Growth Through Coaching](#project-goal-empower-personal-growth-through-coaching)
      - [User Goals](#user-goals)
      - [User Values](#user-values)
      - [User Expectations](#user-expectations)
      - [User Stories](#user-stories)
      - [Strategy Table](#strategy-table)
      - [Trends of modern websites](#trends-of-modern-websites)
  - [Scope](#scope)
  - [Structure](#structure)
  - [Skeleton](#skeleton)
    - [Mobile Wireframe](#mobile-wireframe)
    - [Tablet Wireframe](#tablet-wireframe)
    - [Desktop Wireframe](#desktop-wireframe)
  - [Surface](#surface)
- [Features](#features)
  - [Existing Features](#existing-features)
  - [Features Left to Implement](#features-left-to-implement)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

## UX

### Strategy

#### Project goal: Empower Personal Growth Through Coaching

The primary goal of this project is to create a web application that helps users begin their personal growth journey with the support of a professional coach. To maximize the effectiveness of this journey, users will be asked to complete personality tests that provide deep insights into their behavioral patterns, strengths, and areas for development. 

The platform aims to:
- Lower the barrier to entry for coaching services by offering free personality assessments
- Provide immediate value through preliminary test results to engage visitors
- Connect users with personalized coaching based on their unique personality profiles
- Enable coaches to better understand their clients through data-driven insights
- Create a seamless experience from discovery to ongoing coaching relationship

By combining personality assessment tools with direct coach support, the platform bridges the gap between self-discovery and professional guidance, making personal growth more accessible and effective.

#### User Goals

**Visitor Goals:**
- Understand immediately that the site is about coaching
- Read a clear description of the coach's method to build trust
- See testimonials to increase confidence
- Be invited to take a free test to evaluate the service
- Start a test without immediate registration
- Complete the test quickly with easy-to-answer questions
- See progress during the test
- Receive a preliminary result for immediate value
- Give explicit consent before data is saved
- Understand how personal data will be used

**Registered User Goals:**
- Register easily to save results
- Access account securely (login/logout)
- Recover password when needed
- Modify personal data
- Delete account if desired
- View test history
- Retake tests to compare results over time
- Visualize personality profile clearly
- Download PDF reports
- Receive personalized suggestions based on profile
- Request coaching sessions
- Communicate with the coach
- Receive follow-up emails

**Coach Goals:**
- View list of registered users
- Filter users by personality type
- View detailed user information
- Track user test history
- Add private notes about users
- Mark user status (lead, client, in coaching, completed)
- Create and modify tests
- Define scores and calculation logic
- Activate/deactivate tests
- View test completion statistics
- See how many people have taken the test
- View distribution of profiles
- Track conversion rate between test and registration
- Export data to CSV
- View user consent information
- Delete user data permanently upon request

#### User Values

- **Trust and transparency:** Clear information about the coaching method and data usage
- **Ease of use:** Simple registration, intuitive interfaces, and quick test completion
- **Immediate value:** Preliminary results without barriers
- **Personal growth:** Access to personality profiles and personalized suggestions
- **Privacy control:** Explicit consent and ability to manage personal data
- **Professional support:** Direct communication with coach and follow-up
- **Progress tracking:** History and comparison of results over time

#### User Expectations

**Visitors expect:**
- Clear and immediate understanding of the service
- No obligation to register before trying the test
- Transparent information about data usage
- Professional and trustworthy presentation
- Quick and easy test experience

**Registered Users expect:**
- Secure and reliable account management
- Complete access to test results and history
- Visual and understandable personality profiles
- Downloadable reports
- Direct access to coaching services
- Responsive communication

**Coach expects:**
- Complete user management dashboard
- Flexible test creation and modification tools
- Detailed analytics and statistics
- Data export capabilities
- Full control over user data and privacy compliance

#### User Stories

**Visitor Stories**

*Discover the service*
- As a visitor I want to immediately understand that the site is about coaching so that I know if it's relevant to me
- As a visitor I want to read a clear description of the coach's method so that I can trust them
- As a visitor I want to see testimonials so that I can increase my confidence
- As a visitor I want to be invited to take a free test so that I can evaluate the service

*Take the test*
- As a visitor I want to be able to start a test without registering immediately so that I don't feel blocked
- As a visitor I want to easily answer the questions so that I can complete the test quickly
- As a visitor I want to see a progress bar so that I know how much is left
- As a visitor I want to receive a preliminary result so that I get immediate value
- As a visitor I want to be invited to register to get the complete report so that I can dive deeper

*Privacy*
- As a visitor I want to give explicit consent before my data is saved
- As a visitor I want to know how my data will be used

**Registered User Stories**

*Account*
- As a user I want to register easily so that I can save my results
- As a user I want to login/logout securely
- As a user I want to be able to recover my password
- As a user I want to modify my personal data
- As a user I want to delete my account

*Tests and Results*
- As a user I want to see the history of my tests
- As a user I want to retake a test to compare results over time
- As a user I want to see my personality profile in a clear and visual way
- As a user I want to download a PDF report
- As a user I want to receive personalized suggestions based on my profile

*Coaching*
- As a user I want to be able to request a coaching session
- As a user I want to be able to send a message to the coach
- As a user I want to receive follow-up emails

**Coach (Admin) Stories**

This is the most important part for the platform.

*User Management*
- As a coach I want to see the list of registered users
- As a coach I want to filter users by personality type
- As a coach I want to see the details of each user
- As a coach I want to see the test history of a user
- As a coach I want to add private notes about a user
- As a coach I want to mark the status of a user (lead, client, in coaching, completed)

*Test Management*
- As a coach I want to create a new test
- As a coach I want to modify the questions
- As a coach I want to define scores and calculation logic
- As a coach I want to activate/deactivate a test
- As a coach I want to see test completion statistics

*Dashboard*
- As a coach I want to see how many people have taken the test
- As a coach I want to see the distribution of profiles
- As a coach I want to see the conversion rate between test and registration
- As a coach I want to export data to CSV

*Privacy and Consent*
- As a coach I want to view the consent given by each user
- As a coach I want to be able to permanently delete a user's data upon request

#### Strategy Table

The strategy table illustrates the trade-off between importance and viability. As we move onto Scope soon, it is clear that this project requires different phases to implement the exhaustive list of features - it is an on-going process!

| Opportunity/Problem/Feature | Importance | Viability |
|----------------------------|------------|-----------|
| Personality test without registration | 5 | 5 |
| User registration and authentication | 5 | 5 |
| GDPR consent management | 5 | 4 |
| Preliminary test results display | 5 | 5 |
| Complete personality profile visualization | 5 | 4 |
| Coach dashboard for user management | 5 | 3 |
| User test history and tracking | 4 | 4 |
| Landing page with coach method description | 4 | 5 |
| Testimonials section | 4 | 5 |
| PDF report generation | 4 | 3 |
| User status tracking (lead, client, etc.) | 4 | 4 |
| Coach private notes on users | 4 | 5 |
| Personalized suggestions based on profile | 4 | 3 |
| Test completion statistics and analytics | 4 | 3 |
| Filter users by personality type | 3 | 4 |
| Progress bar during test | 3 | 5 |
| Password recovery system | 3 | 4 |
| Coaching session request system | 3 | 2 |
| Email follow-up automation | 3 | 3 |
| Dynamic test creation and modification | 3 | 2 |
| Profile comparison over time | 3 | 3 |
| Direct messaging between user and coach | 2 | 2 |
| CSV data export | 2 | 5 |
| Account deletion | 2 | 4 |
| **Total** | **89** | **91** |

The table shows that while the project has high strategic value (importance = 89), many features are technically viable (viability = 91), though some advanced features like dynamic test creation and messaging systems require more complex implementation and will be developed in later phases.

#### Trends of modern websites

Modern coaching websites are evolving to meet user expectations for personalized, engaging, and trustworthy experiences. Key trends that influence this project include:

**Interactive Assessment Tools**
- Personality tests and quizzes as lead generation tools
- Immediate feedback and preliminary results to engage visitors
- Gamification elements to increase completion rates
- Progress indicators and visual feedback

**Personalization**
- Tailored content based on user profiles and test results
- Customized recommendations and coaching paths
- Dynamic user dashboards showing individual progress
- Adaptive content that responds to user behavior

**Trust and Transparency**
- Prominent display of coach credentials and methodology
- Authentic testimonials with photos and detailed stories
- Clear privacy policies and GDPR compliance
- Transparent pricing and service descriptions

**Mobile-First Design**
- Responsive layouts that work seamlessly across all devices
- Touch-friendly interfaces for assessments
- Fast loading times and optimized performance
- Progressive Web App capabilities

**Data Visualization**
- Visual personality profiles using charts and graphics
- Progress tracking with intuitive dashboards
- Analytics and insights presented in digestible formats
- Comparison tools for tracking growth over time

**User-Centric Features**
- Minimal registration barriers (guest access)
- Seamless authentication and account management
- Easy access to past results and reports
- Downloadable resources (PDF reports)

**Professional Coach Tools**
- Comprehensive admin dashboards
- Client management systems
- Analytics and reporting capabilities
- CRM-like features for tracking client relationships

**Communication Integration**
- Direct messaging or contact forms
- Email automation for follow-ups
- Booking systems for scheduling sessions
- Video consultation capabilities (future consideration)

This project incorporates these trends by offering a frictionless test experience, personalized results, transparent data handling, and robust tools for both users and coaches to facilitate meaningful personal growth journeys.

### Scope

Based on the strategy table analysis and the trade-off between importance and viability, the project will be developed in multiple phases. This phased approach ensures that we deliver a functional minimum viable product (MVP) quickly while maintaining the flexibility to expand features based on user feedback and technical feasibility.

The development is structured to prioritize high-importance, high-viability features first, establishing a solid foundation before adding more complex functionalities. Each phase builds upon the previous one, creating an iterative process that allows for continuous improvement and adaptation.

#### Phase 1: MVP - Core Assessment Platform

**Goal:** Launch a functional platform that allows visitors to take personality tests and coaches to manage basic user data.

**Features:**
- Landing page with coach method description and testimonials
- Personality test accessible without registration
- Progress bar and user-friendly test interface
- Preliminary test results display
- GDPR consent management and privacy policy
- User registration and authentication system
- Secure login/logout functionality
- Basic coach dashboard to view registered users
- User profile visualization with personality results

**Timeline:** 8-10 weeks

**Success Criteria:** Visitors can complete a test, register, and view their results; coach can access user data and test results.

#### Phase 2: Enhanced User Experience

**Goal:** Enrich the user experience with advanced features for result management and coach tools.

**Features:**
- Complete personality profile visualization with charts/graphics
- User test history and tracking
- PDF report generation and download
- Coach private notes on users
- User status tracking (lead, client, in coaching, completed)
- Filter users by personality type
- Password recovery system
- Account settings and data modification
- Test completion statistics and analytics dashboard

**Timeline:** 6-8 weeks

**Success Criteria:** Users can access comprehensive results and download reports; coaches have robust tools for client management.

#### Phase 3: Personalization and Engagement

**Goal:** Add personalized features and improve user engagement through targeted content and coaching integration.

**Features:**
- Personalized suggestions based on personality profile
- Profile comparison over time
- Ability to retake tests and track progress
- Coaching session request system
- Email follow-up automation
- Enhanced analytics (conversion rates, profile distribution)
- CSV data export for coaches
- Account deletion functionality
- Testimonials management system

**Timeline:** 6-8 weeks

**Success Criteria:** Users receive personalized guidance; automated communication increases engagement; coaches can track business metrics.

#### Phase 4: Advanced Features and Optimization

**Goal:** Implement advanced features for comprehensive platform functionality and optimize performance.

**Features:**
- Dynamic test creation and modification tools for coaches
- Direct messaging between users and coach
- Enhanced booking/scheduling system
- Advanced CRM features for coaches
- Performance optimizations and mobile enhancements
- Additional data visualization and reporting tools
- Integration capabilities (calendar, email services, etc.)
- A/B testing for conversion optimization

**Timeline:** 8-10 weeks

**Success Criteria:** Platform offers complete coaching management ecosystem; excellent performance across all devices; high user satisfaction.

#### Future Considerations

Beyond Phase 4, potential enhancements based on user feedback may include:
- Video consultation integration
- Group coaching features
- Mobile native applications
- API for third-party integrations
- Multi-language support
- Advanced AI-driven personality insights

This phased approach ensures that each development cycle delivers value while maintaining code quality, security, and user experience standards.

### Structure

The structure of the platform is designed to leverage users' prior experience with modern web applications, following established conventions and familiar patterns that reduce cognitive load and improve usability. By aligning with user expectations, we create an intuitive experience that requires minimal learning.

#### Information Architecture

The platform follows a hierarchical structure with clear parent-child relationships:

```
Homepage (Public)
├── About/Coach Method
├── Testimonials
├── Take Test (Guest Access)
│   ├── Test Questions
│   ├── Progress Tracking
│   └── Preliminary Results
├── Login/Register
└── Privacy Policy/Terms

User Dashboard (Authenticated)
├── My Profile
│   ├── Personality Profile
│   ├── Test History
│   └── Account Settings
├── Take New Test
├── View Results
│   ├── Detailed Analysis
│   ├── Download PDF
│   └── Personalized Suggestions
├── Contact Coach
└── Logout

Coach Dashboard (Admin)
├── Users Overview
│   ├── User List (filterable)
│   ├── User Details
│   ├── Add Notes
│   └── Status Management
├── Analytics
│   ├── Test Statistics
│   ├── Conversion Metrics
│   └── Profile Distribution
├── Test Management
│   ├── Create/Edit Tests
│   ├── Questions Library
│   └── Scoring Logic
├── Messages/Requests
└── Export Data
```

#### Leveraging Familiar Patterns

**Navigation Conventions**
- **Top Navigation Bar:** Logo on the left (clickable home link), main menu items in the center, login/account on the right
- **Hamburger Menu:** On mobile devices, collapsible navigation follows the standard pattern
- **Breadcrumbs:** Clear path indication for deeper pages (e.g., Dashboard > Test History > Test Details)
- **Footer:** Secondary links, social media, contact information, and legal links (common pattern users expect)

**Authentication Flow**
- Standard login/register forms with email and password fields
- "Remember me" checkbox and "Forgot password?" link positioned as users expect
- OAuth options (Google, Facebook) as alternative login methods - recognized pattern
- Clear visual separation between login and registration
- Email verification process following industry standards

**Dashboard Layout**
- **Sidebar Navigation:** Persistent left sidebar with main sections (common in SaaS applications)
- **Welcome Header:** Personalized greeting with user name (establishes context)
- **Card-Based Layout:** Information grouped in visual cards (familiar from social media, admin panels)
- **Action Buttons:** Primary actions clearly highlighted (CTA buttons in predictable locations)

**Form Design**
- Single-column forms for better mobile experience (industry best practice)
- Labels above input fields (most scannable and familiar pattern)
- Inline validation with clear error messages
- Progress indication for multi-step processes (test completion)
- Clear submit buttons with action-oriented text ("Continue", "Submit", "Save")

**Data Presentation**
- **Tables:** For lists of users, test results (with sortable columns, pagination)
- **Charts/Graphs:** For personality profiles and analytics (using common chart types: pie, bar, line)
- **Icons:** Universally recognized icons (home, user, settings, logout, download, etc.)
- **Status Indicators:** Color-coded badges (green for active, yellow for pending, etc.)

**Content Organization**
- **F-Pattern Layout:** Important information follows natural eye movement (top-left to right)
- **Visual Hierarchy:** Size, color, and spacing guide attention to key elements
- **White Space:** Adequate breathing room between sections (reduces overwhelm)
- **Consistent Spacing:** Uniform margins and padding throughout (professional feel)

#### Interaction Design

**Predictable Behaviors**
- Links change color/underline on hover (standard web convention)
- Buttons show hover states and loading states during actions
- Clickable elements have appropriate cursor changes
- Modal dialogs for confirmations and additional information
- Toast notifications for success/error feedback (non-intrusive)

**Feedback Mechanisms**
- Loading spinners during data fetching
- Success messages after form submissions
- Error alerts with clear, actionable guidance
- Disabled states for unavailable actions
- Real-time validation during form completion

**Progressive Disclosure**
- Show basic information first, reveal details on demand
- Expandable sections for advanced features
- Tooltips for additional context without cluttering interface
- Collapsible admin panels for dense information

#### User Flow Optimization

**Guest to Registered User Journey**
1. Land on homepage → Clear value proposition
2. Encouraged to take test → Prominent CTA button
3. Complete test without barriers → Low friction experience
4. View preliminary results → Immediate value
5. Prompted to register for full report → Clear benefit
6. Simple registration form → Minimal fields required
7. Access full dashboard → Seamless transition

**Registered User Flow**
1. Login → Direct to personalized dashboard
2. See test history and profile → Context established
3. Take new test or view past results → Clear options
4. Download reports or contact coach → Easy access to value

**Coach Workflow**
1. Login → Admin dashboard with key metrics
2. View recent user activity → Immediate insights
3. Filter/search users → Efficient management
4. Access individual user details → Complete information
5. Add notes or update status → Quick actions
6. View analytics → Business intelligence

#### Consistency Principles

- **Visual Consistency:** Same components look and behave identically throughout
- **Content Consistency:** Tone, terminology, and messaging remain uniform
- **Functional Consistency:** Similar actions work the same way across different pages
- **External Consistency:** Follows web standards and platform conventions (iOS, Android guidelines for mobile)

By following these established patterns and conventions, users can rely on their existing mental models, reducing learning time and increasing confidence in using the platform. This familiar structure creates a comfortable environment where users can focus on their personal growth journey rather than figuring out how to navigate the interface.

### Skeleton

#### Mobile Wireframe

#### Tablet Wireframe

#### Desktop Wireframe

### Surface

## Features

### Existing Features

### Features Left to Implement

## Technologies Used

## Testing

## Deployment

## Credits
