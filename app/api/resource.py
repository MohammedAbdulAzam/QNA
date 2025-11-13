from flask_restful import Api, Resource, reqparse
from flask import jsonify, request
from app.models import Subject, db




# Request parser setup
subject_parser = reqparse.RequestParser()
subject_parser.add_argument('name', type=str, required=True, 
                          help='Subject name is required', location='json')
subject_parser.add_argument('description', type=str, 
                          required=False, location='json')

class SubjectListResource(Resource):
    def get(self):
        """Get all subjects"""
        subjects = Subject.query.all()
        return jsonify([{
            'id': s.id,
            'name': s.name,
            'description': s.description,
            'created_at': s.created_at.isoformat() if s.created_at else None
        } for s in subjects])

    def post(self):
        """Create new subject"""
        args = subject_parser.parse_args()
        subject = Subject(name=args['name'], description=args.get('description'))
        db.session.add(subject)
        db.session.commit()
        return jsonify({
            'id': subject.id,
            'name': subject.name,
            'description': subject.description,
            'created_at': subject.created_at.isoformat()
        }), 201

class SubjectResource(Resource):
    def get(self, subject_id):
        """Get single subject"""
        subject = Subject.query.get_or_404(subject_id)
        return jsonify({
            'id': subject.id,
            'name': subject.name,
            'description': subject.description,
            'created_at': subject.created_at.isoformat()
        })

    def put(self, subject_id):
        """Update subject"""
        subject = Subject.query.get_or_404(subject_id)
        args = subject_parser.parse_args()
        
        subject.name = args['name']
        if args['description'] is not None:
            subject.description = args['description']
            
        db.session.commit()
        return jsonify({
            'id': subject.id,
            'name': subject.name,
            'description': subject.description,
            'created_at': subject.created_at.isoformat()
        })

    def delete(self, subject_id):
        """Delete subject"""
        subject = Subject.query.get_or_404(subject_id)
        db.session.delete(subject)
        db.session.commit()
        return jsonify({'message': 'Subject deleted successfully'})

