#!/usr/bin/env python3
"""
Web Frontend for Drug Repositioning Agent
Flask-based web application with real-time analysis
"""

import os
import sys
import json
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import threading
import uuid

from drug_repositioning_agent import (
    create_drug_repositioning_graph, 
    MolecularAnalysis,
    DrugCandidate,
    DrugCandidateList
)
from langchain_core.messages import HumanMessage, AIMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'drug-repo-secret-key-2024')

# Initialize SocketIO
socketio = SocketIO(app, cors_allowed_origins="*")

# Global storage for analysis sessions
analysis_sessions = {}
analysis_history = []

class WebDrugRepositioningAgent:
    def __init__(self):
        self.llm = None
        
    def initialize_llm(self):
        """Initialize Claude LLM"""
        try:
            self.llm = ChatAnthropic(
                model="claude-3-5-sonnet-20241022",
                anthropic_api_key=os.getenv("ANTHROPIC_API_KEY"),
                temperature=0.3
            )
            return True
        except Exception as e:
            return False, str(e)
    
    def analyze_disease(self, user_input, session_id, dry_run=False):
        """Analyze disease with real-time updates via SocketIO"""
        
        if dry_run:
            return self.simulate_analysis(user_input, session_id)
        
        if not self.llm:
            success, error = self.initialize_llm()
            if not success:
                socketio.emit('analysis_error', {
                    'error': f'Failed to initialize AI model: {error}'
                }, room=session_id)
                return None
        
        try:
            # Step 1: Molecular Analysis
            socketio.emit('analysis_progress', {
                'step': 1,
                'step_name': 'Molecular Pathology Analysis',
                'message': 'Analyzing molecular mechanisms...',
                'progress': 10
            }, room=session_id)
            
            molecular_analysis = self._perform_molecular_analysis(user_input, session_id)
            
            socketio.emit('analysis_progress', {
                'step': 1,
                'step_name': 'Molecular Pathology Analysis',
                'message': 'Molecular analysis complete',
                'progress': 33,
                'data': {
                    'disease_name': molecular_analysis.disease_name,
                    'molecular_markers': molecular_analysis.molecular_markers
                }
            }, room=session_id)
            
            # Step 2: Drug Identification
            socketio.emit('analysis_progress', {
                'step': 2,
                'step_name': 'Drug Candidate Identification',
                'message': 'Identifying potential drug candidates...',
                'progress': 40
            }, room=session_id)
            
            drug_candidates = self._identify_drug_candidates(molecular_analysis, session_id)
            
            socketio.emit('analysis_progress', {
                'step': 2,
                'step_name': 'Drug Candidate Identification',
                'message': f'Found {len(drug_candidates.candidates)} potential candidates',
                'progress': 66,
                'data': {
                    'candidates': [
                        {
                            'drug_name': c.drug_name,
                            'approval_status': c.approval_status,
                            'current_applications': c.current_applications,
                            'molecular_rationale': c.molecular_rationale,
                            'shared_pathology': c.shared_pathology
                        } for c in drug_candidates.candidates
                    ]
                }
            }, room=session_id)
            
            # Step 3: Filtering
            socketio.emit('analysis_progress', {
                'step': 3,
                'step_name': 'Candidate Filtering',
                'message': 'Filtering and validating candidates...',
                'progress': 75
            }, room=session_id)
            
            filter_analysis = self._filter_candidates(molecular_analysis, drug_candidates, session_id)
            
            # Final results
            result = {
                'molecular_analysis': {
                    'disease_name': molecular_analysis.disease_name,
                    'molecular_markers': molecular_analysis.molecular_markers,
                    'sources': molecular_analysis.sources
                },
                'drug_candidates': [
                    {
                        'drug_name': c.drug_name,
                        'approval_status': c.approval_status,
                        'current_applications': c.current_applications,
                        'molecular_rationale': c.molecular_rationale,
                        'shared_pathology': c.shared_pathology
                    } for c in drug_candidates.candidates
                ],
                'filter_analysis': filter_analysis,
                'timestamp': datetime.now().isoformat(),
                'user_input': user_input
            }
            
            # Store in history
            analysis_history.append(result)
            
            socketio.emit('analysis_complete', {
                'message': 'Analysis complete!',
                'progress': 100,
                'result': result
            }, room=session_id)
            
            return result
            
        except Exception as e:
            socketio.emit('analysis_error', {
                'error': f'Analysis failed: {str(e)}'
            }, room=session_id)
            return None
    
    def _perform_molecular_analysis(self, user_input, session_id):
        """Perform molecular pathology analysis"""
        analysis_prompt = ChatPromptTemplate.from_template("""
        You are a molecular pathologist. Analyze the provided input and identify key molecular markers including:
        - Genetic mutations
        - Cellular abnormalities
        - Affected molecular pathways
        - Protein expression changes
        - Other molecular phenotypes
        
        If a disease name is provided, identify its molecular characteristics.
        If molecular observations are provided, categorize and analyze them.
        
        Provide comprehensive molecular characterization with sources.
        
        Input: {user_input}
        """)
        
        structured_llm = self.llm.with_structured_output(MolecularAnalysis)
        chain = analysis_prompt | structured_llm
        
        return chain.invoke({"user_input": user_input})
    
    def _identify_drug_candidates(self, molecular_analysis, session_id):
        """Identify drug repositioning candidates"""
        drug_prompt = ChatPromptTemplate.from_template("""
        You are an expert in drug repositioning and molecular pathology. 
        Based on the molecular markers provided, identify existing drugs that could be repurposed.
        
        Focus on:
        1. Drugs targeting similar molecular pathways
        2. Drugs used for diseases with similar molecular abnormalities
        3. Drugs affecting the same cellular processes
        
        For each candidate, provide:
        - Drug name
        - Current approval status
        - Current applications
        - Detailed molecular rationale for repositioning
        - Specific shared molecular pathology
        
        Disease/Condition: {disease_name}
        Molecular markers: {molecular_markers}
        """)
        
        drug_structured_llm = self.llm.with_structured_output(DrugCandidateList)
        drug_chain = drug_prompt | drug_structured_llm
        
        return drug_chain.invoke({
            "disease_name": molecular_analysis.disease_name,
            "molecular_markers": molecular_analysis.molecular_markers
        })
    
    def _filter_candidates(self, molecular_analysis, drug_candidates, session_id):
        """Filter and validate drug candidates"""
        filter_prompt = ChatPromptTemplate.from_template("""
        Review these drug candidates for {disease_name} repositioning:
        
        {candidates}
        
        Remove any drugs that are:
        1. Already approved or in trials for this specific condition
        2. Would not logically help with the identified molecular pathology
        3. Have weak molecular rationale
        
        Return only the most promising candidates with strong scientific rationale.
        Explain your filtering decisions.
        """)
        
        candidates_text = "\n".join([
            f"- {c.drug_name}: {c.molecular_rationale}" 
            for c in drug_candidates.candidates
        ])
        
        filter_response = self.llm.invoke(filter_prompt.format_messages(
            disease_name=molecular_analysis.disease_name,
            candidates=candidates_text
        ))
        
        return filter_response.content
    
    def simulate_analysis(self, user_input, session_id):
        """Simulate analysis for demo mode"""
        steps = [
            {'step': 1, 'name': 'Molecular Analysis', 'progress': 33},
            {'step': 2, 'name': 'Drug Identification', 'progress': 66},
            {'step': 3, 'name': 'Filtering', 'progress': 100}
        ]
        
        for step in steps:
            time.sleep(1)  # Simulate processing time
            socketio.emit('analysis_progress', {
                'step': step['step'],
                'step_name': step['name'],
                'message': f'Processing {step["name"]}...',
                'progress': step['progress']
            }, room=session_id)
        
        # Mock result
        result = {
            'molecular_analysis': {
                'disease_name': f'Simulated analysis for: {user_input}',
                'molecular_markers': {
                    'example_mutations': ['Mock mutation 1', 'Mock mutation 2'],
                    'example_pathways': ['Mock pathway 1', 'Mock pathway 2'],
                    'example_abnormalities': ['Mock abnormality 1', 'Mock abnormality 2']
                },
                'sources': ['Mock Database', 'Simulated Research']
            },
            'drug_candidates': [
                {
                    'drug_name': 'Example Drug A',
                    'approval_status': 'FDA Approved',
                    'current_applications': ['Condition X', 'Condition Y'],
                    'molecular_rationale': 'Mock molecular rationale for repositioning',
                    'shared_pathology': 'Simulated shared pathology'
                },
                {
                    'drug_name': 'Example Drug B',
                    'approval_status': 'Investigational',
                    'current_applications': ['Condition Z'],
                    'molecular_rationale': 'Another mock rationale',
                    'shared_pathology': 'Another simulated pathology'
                }
            ],
            'filter_analysis': 'Simulated filtering - this would remove inappropriate candidates',
            'timestamp': datetime.now().isoformat(),
            'user_input': user_input
        }
        
        socketio.emit('analysis_complete', {
            'message': 'Simulation complete!',
            'progress': 100,
            'result': result
        }, room=session_id)
        
        return result

# Initialize the agent
agent = WebDrugRepositioningAgent()

# Routes
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """Check API status"""
    has_api_key = bool(os.getenv("ANTHROPIC_API_KEY"))
    return jsonify({
        'api_key_configured': has_api_key,
        'dry_run_available': True
    })

@app.route('/api/history')
def get_history():
    """Get analysis history"""
    return jsonify(analysis_history[-10:])  # Return last 10 analyses

@app.route('/api/analyze', methods=['POST'])
def start_analysis():
    """Start analysis (returns immediately, actual analysis happens via SocketIO)"""
    data = request.json
    user_input = data.get('user_input', '').strip()
    dry_run = data.get('dry_run', False)
    
    if not user_input:
        return jsonify({'error': 'Please provide a disease name or molecular pathology'}), 400
    
    # Generate session ID
    session_id = str(uuid.uuid4())
    
    # Store session
    analysis_sessions[session_id] = {
        'user_input': user_input,
        'dry_run': dry_run,
        'started_at': datetime.now().isoformat(),
        'status': 'starting'
    }
    
    return jsonify({'session_id': session_id})

# SocketIO Events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('join_analysis')
def handle_join_analysis(data):
    """Join analysis session"""
    session_id = data.get('session_id')
    if session_id in analysis_sessions:
        # Join room for this analysis
        # Start analysis in background thread
        thread = threading.Thread(
            target=agent.analyze_disease,
            args=(
                analysis_sessions[session_id]['user_input'],
                request.sid,
                analysis_sessions[session_id]['dry_run']
            )
        )
        thread.daemon = True
        thread.start()
    else:
        emit('analysis_error', {'error': 'Invalid session ID'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    # Check if running in production or development
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    port = int(os.getenv('PORT', 5000))
    
    if debug_mode:
        socketio.run(app, debug=True, host='0.0.0.0', port=port)
    else:
        # Production server
        from waitress import serve
        socketio.run(app, host='0.0.0.0', port=port) 