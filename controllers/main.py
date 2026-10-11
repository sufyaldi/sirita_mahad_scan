# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request, Response
import json

class SatpamScanController(http.Controller):

    @http.route('/mahad/satpam/scan', type='http', auth="user", website=True)
    def satpam_scan_page(self, **kw):
        """Halaman Web Scanner Kamera Khusus Petugas Keamanan"""
        user = request.env.user
        is_satpam = user.has_group('sirita_mahad_scan.group_hostel_satpam') or \
                    user.has_group('sirita_mahad.group_hostel_manager') or \
                    user.has_group('sirita_mahad.group_hostel_admin')

        if not is_satpam:
            return request.render("website.403", {'message': 'Akses Ditolak: Halaman scanner ini khusus untuk Petugas Keamanan asrama.'})

        values = {
            'page_name': 'satpam_scan',
        }
        return request.render("sirita_mahad_scan.satpam_scan_page", values)

    @http.route('/api/mahad/gate/verify', type='http', auth="user", methods=['POST'], csrf=False)
    def gate_verify_qr(self, token=None, action='checkout', **kw):
        """API Verification & Execution untuk Scanner Satpam"""
        if not token:
            return Response(json.dumps({'status': 'error', 'message': 'Kode Token QR Kosong'}), content_type='application/json', status=400)

        token = token.strip().upper()
        permit = request.env['mahad.permit'].sudo().search([('qr_code_token', '=', token)], limit=1)

        if not permit:
            return Response(json.dumps({
                'status': 'error',
                'message': f'Izin dengan Token [{token}] Tidak Ditemukan!'
            }), content_type='application/json', status=404)

        student_name = permit.student_id.name
        permit_type_str = "Izin Pesiar (Siang/Sore)" if permit.permit_type == 'pesiar' else "Izin Bermalam"

        if action == 'checkout':
            if permit.state in ('draft', 'cancelled'):
                return Response(json.dumps({
                    'status': 'error',
                    'message': f'DITOLAK: Surat Izin {permit.name} milik {student_name} BELUM DISETUJUI Musyrif!'
                }), content_type='application/json', status=400)
            
            if permit.state == 'checked_out':
                return Response(json.dumps({
                    'status': 'warning',
                    'message': f'PERINGATAN: {student_name} SUDAH BERSTATUS KELUAR ASRAMA sebelumnya.'
                }), content_type='application/json', status=200)

            permit.sudo().action_scan_checkout()
            return Response(json.dumps({
                'status': 'success',
                'message': f'ACC KELUAR: {student_name} Diizinkan Keluar Kompleks.',
                'permit_number': permit.name,
                'student_name': student_name,
                'permit_type': permit_type_str,
                'destination': permit.destination,
                'action_taken': 'CHECK-OUT (KELUAR)'
            }), content_type='application/json', status=200)

        elif action == 'checkin':
            if permit.state == 'checked_in':
                return Response(json.dumps({
                    'status': 'warning',
                    'message': f'PERINGATAN: {student_name} SUDAH BERSTATUS KEMBALI di asrama.'
                }), content_type='application/json', status=200)

            permit.sudo().action_scan_checkin()
            late_msg = " (TERLAMBAT KEMBALI - POIN TERCATAT)" if permit.is_late else ""
            return Response(json.dumps({
                'status': 'success',
                'message': f'ACC KEMBALI: {student_name} Telah Kembali Ke Asrama{late_msg}.',
                'permit_number': permit.name,
                'student_name': student_name,
                'permit_type': permit_type_str,
                'is_late': permit.is_late,
                'action_taken': 'CHECK-IN (KEMBALI)'
            }), content_type='application/json', status=200)

        return Response(json.dumps({'status': 'error', 'message': 'Aksi tidak valid'}), content_type='application/json', status=400)
