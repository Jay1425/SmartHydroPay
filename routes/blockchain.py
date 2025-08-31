from flask import Blueprint, request, jsonify
from blockchain.web3_utils import get_web3_utils
from app.models import SubsidyLog, db

blockchain_bp = Blueprint('blockchain_bp', __name__)

@blockchain_bp.route('/register_producer', methods=['POST'])
def register_producer():
    data = request.get_json()
    producer_address = data.get('producer_address')
    if not producer_address:
        return jsonify({'error': 'Producer address is required'}), 400

    try:
        web3_utils = get_web3_utils()
        receipt = web3_utils.register_producer(producer_address)
        
        log = SubsidyLog(
            producer_address=producer_address,
            action='register_producer',
            tx_hash=receipt.transactionHash.hex()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'status': 'success', 'tx_hash': receipt.transactionHash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blockchain_bp.route('/set_milestone', methods=['POST'])
def set_milestone():
    data = request.get_json()
    producer_address = data.get('producer_address')
    target_volume = data.get('target_volume')
    subsidy_amount = data.get('subsidy_amount')

    if not all([producer_address, target_volume, subsidy_amount]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        web3_utils = get_web3_utils()
        receipt = web3_utils.set_milestone(producer_address, target_volume, subsidy_amount)
        
        log = SubsidyLog(
            producer_address=producer_address,
            action='set_milestone',
            details={'target_volume': target_volume, 'subsidy_amount': subsidy_amount},
            tx_hash=receipt.transactionHash.hex()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'status': 'success', 'tx_hash': receipt.transactionHash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@blockchain_bp.route('/verify_and_release', methods=['POST'])
def verify_and_release():
    data = request.get_json()
    producer_address = data.get('producer_address')
    actual_volume = data.get('actual_volume')

    if not all([producer_address, actual_volume]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        web3_utils = get_web3_utils()
        receipt = web3_utils.verify_and_release(producer_address, actual_volume)
        
        log = SubsidyLog(
            producer_address=producer_address,
            action='verify_and_release',
            details={'actual_volume': actual_volume},
            tx_hash=receipt.transactionHash.hex()
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'status': 'success', 'tx_hash': receipt.transactionHash.hex()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
