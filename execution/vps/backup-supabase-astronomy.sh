#!/bin/bash
# Nightly copy of the Astronomy Supabase DB (ref qeakrjnseboiulcojlcw) with the read-only role backup_reader.
# Saves /opt/backups/supabase-astronomy-YYYY-MM-DD.dump (14 days, same as the bot DBs) and alerts Facu on
# Telegram if anything fails or the dump looks empty. Storage files (photos) live in S3 and are NOT in this dump.
set -u
ENV=/opt/astronomy/supabase-backup.env
OUT=/opt/backups/supabase-astronomy-$(date +%F).dump
alert() {
  rm -f "$OUT.tmp"
  [ -n "${TELEGRAM_BOT_TOKEN:-}" ] && curl -s -m 20 "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/sendMessage" \
    --data-urlencode chat_id="$TELEGRAM_CHAT_ID" --data-urlencode text="🔴 Backup de la base de Academy FALLÓ ($(date +%F)): $1" >/dev/null
  echo "FAIL: $1" >&2; exit 1
}
set -a; . "$ENV" || alert "no encuentro $ENV"
set +a; [ -n "${PGPASSWORD:-}" ] || alert "falta PGPASSWORD en $ENV"
docker run --rm -e PGPASSWORD postgres:17-alpine pg_dump -Fc \
  -h aws-1-us-east-2.pooler.supabase.com -p 5432 -U backup_reader.qeakrjnseboiulcojlcw -d postgres \
  --schema=public --schema=auth --schema=storage --schema=cron --no-owner --no-privileges > "$OUT.tmp" 2> /tmp/supabase-backup.err \
  || alert "pg_dump: $(tail -c 300 /tmp/supabase-backup.err)"
SIZE=$(stat -c %s "$OUT.tmp")
[ "$SIZE" -gt 500000 ] || alert "el archivo pesa $SIZE bytes, sospechoso de vacío"
TABLES=$(docker run --rm -i postgres:17-alpine pg_restore --list < "$OUT.tmp" | grep -c "TABLE DATA public")
[ "$TABLES" -gt 20 ] || alert "sólo $TABLES tablas de public con datos"
mv "$OUT.tmp" "$OUT"
find /opt/backups -name "supabase-astronomy-*.dump" -mtime +14 -delete
echo "OK $OUT $SIZE bytes, $TABLES tablas public"
