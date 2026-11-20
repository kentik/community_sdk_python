// Minimal copy of ui-app's createWrapper path: camelify(call) on a grpc-js unary call.
const fs = require('fs');
const os = require('os');
const path = require('path');
const _ = require('lodash');
const grpc = require('@grpc/grpc-js');
const loader = require('@grpc/proto-loader');

const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'kentik-grpc-deadline-'));
const protoPath = path.join(tempDir, 't.proto');

// Verbatim from kentik/ui-app src/shared/util/changeCase.js
const camelify = (obj) =>
  _.transform(obj, (acc, value, key, target) => {
    const camelKey = _.isArray(target) ? key : _.camelCase(key);
    acc[camelKey] = _.isObject(value) ? camelify(value) : value;
  });

fs.writeFileSync(protoPath, 'syntax = "proto3"; package t; message M { string name = 1; } service S { rpc Get(M) returns (M); }');
const t = grpc.loadPackageDefinition(loader.loadSync(protoPath)).t;

const server = new grpc.Server();
server.addService(t.S.service, {
  Get: (call, callback) => {
    try {
      camelify(call);
      callback(null, { name: 'ok' });
    } catch (e) {
      callback({ code: grpc.status.INTERNAL, details: `internal error (name:${e.name}) ${e.message}` });
    }
  },
});

server.bindAsync('127.0.0.1:0', grpc.ServerCredentials.createInsecure(), async (err, port) => {
  if (err) {
    console.error(err);
    fs.rmSync(tempDir, { recursive: true, force: true });
    process.exitCode = 1;
    return;
  }
  const client = new t.S(`127.0.0.1:${port}`, grpc.credentials.createInsecure());
  const call = (label, options) =>
    new Promise((resolve) =>
      client.Get({ name: 'x' }, new grpc.Metadata(), options, (e, r) => {
        console.log(label.padEnd(24), e ? `ERROR ${e.details}` : `OK ${r.name}`);
        resolve();
      }),
    );
  try {
    await call('no deadline', {});
    await call('deadline 1 s', { deadline: Date.now() + 1000 });
    await call('deadline 30 s', { deadline: Date.now() + 30000 });
    await call('deadline 300 s', { deadline: Date.now() + 300000 });
  } finally {
    client.close();
    server.forceShutdown();
    fs.rmSync(tempDir, { recursive: true, force: true });
  }
});
