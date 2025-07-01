#!/usr/bin/env node
/**
 * Memory Test Harness for Socratic Shell
 * 
 * Tests Claude Code interaction patterns for memory bank implementation.
 * Uses node-pty for reliable terminal interaction.
 */

import * as pty from 'node-pty';

interface TestResult {
    success: boolean;
    found: string[];
    missing?: string[];
    responseLength: number;
}

interface BootTestResult extends TestResult {
    missing: string[];
}

interface ConsolidationTestResult extends TestResult {}

class ClaudeTestHarness {
    private ptyProcess: pty.IPty | null = null;
    private output: string = '';
    private isReady: boolean = false;

    async start(): Promise<boolean> {
        console.log('🚀 Starting Claude Code with node-pty...');
        
        // Spawn Claude Code with proper environment
        this.ptyProcess = pty.spawn('/home/nikomatsakis/.claude/local/claude', [], {
            name: 'xterm-256color',
            cols: 120,
            rows: 40,
            cwd: process.cwd(),
            env: process.env
        });

        // Set up data handlers
        this.ptyProcess.onData((data: string) => {
            this.output += data;
            // Look for readiness indicators
            if (data.includes('>') || data.includes('claude')) {
                this.isReady = true;
            }
        });

        this.ptyProcess.onExit(({ exitCode, signal }) => {
            console.log(`Claude exited with code ${exitCode}, signal ${signal}`);
        });

        // Wait for Claude to be ready
        console.log('⏳ Waiting for Claude to be ready...');
        await this.waitForReady();
        console.log('✅ Claude is ready!');
        
        return true;
    }

    private async waitForReady(timeout: number = 30000): Promise<void> {
        const start = Date.now();
        while (!this.isReady && (Date.now() - start) < timeout) {
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        if (!this.isReady) {
            throw new Error('Timeout waiting for Claude to be ready');
        }
    }

    async sendMessage(message: string): Promise<string> {
        if (!this.ptyProcess) {
            throw new Error('Claude process not started');
        }

        console.log(`📤 Sending: ${message}`);
        
        // Clear output buffer
        this.output = '';
        
        // Send message and submit with Enter keys
        this.ptyProcess.write(message);
        await new Promise(resolve => setTimeout(resolve, 100));
        this.ptyProcess.write('\r');
        await new Promise(resolve => setTimeout(resolve, 100));
        this.ptyProcess.write('\x0D');
        
        // Wait for response
        await this.waitForResponse();
        
        // Clean up the output
        const cleanOutput = this.stripAnsi(this.output);
        console.log(`📨 Response length: ${cleanOutput.length} characters`);
        
        return cleanOutput;
    }

    private async waitForResponse(timeout: number = 60000): Promise<void> {
        const start = Date.now();
        let stableCount = 0;
        let lastLength = 0;
        
        console.log('⏳ Waiting for response...');
        
        while ((Date.now() - start) < timeout) {
            await new Promise(resolve => setTimeout(resolve, 500));
            
            // Check if output has stabilized
            if (this.output.length === lastLength) {
                stableCount++;
                if (stableCount >= 6) { // Stable for 3 seconds
                    console.log('✅ Output appears stable');
                    break;
                }
            } else {
                stableCount = 0;
                lastLength = this.output.length;
            }
        }
        
        if ((Date.now() - start) >= timeout) {
            console.log('⏰ Timeout reached');
        }
    }

    private stripAnsi(text: string): string {
        // Remove ANSI escape sequences
        return text.replace(/\x1b\[[0-9;]*[mGKHJA-Z]/g, '');
    }

    close(): void {
        if (this.ptyProcess) {
            this.ptyProcess.kill();
        }
    }
}

/**
 * Test scenarios for memory bank implementation
 */
class MemoryBankTests {
    constructor(private harness: ClaudeTestHarness) {}

    async testBootProcedure(): Promise<BootTestResult> {
        console.log('\n=== Memory Test: Boot Procedure ===');
        const response = await this.harness.sendMessage('Hi again, Claude!');
        
        const indicators = [
            'Prime Directive',
            'Make it so', 
            'partnership',
            'hooks',
            'completion'
        ] as const;
        
        console.log('🔍 Checking for boot procedure patterns:');
        const found: string[] = [];
        for (const indicator of indicators) {
            if (response.toLowerCase().includes(indicator.toLowerCase())) {
                console.log(`🎉 FOUND: ${indicator}`);
                found.push(indicator);
            } else {
                console.log(`❌ Missing: ${indicator}`);
            }
        }
        
        const missing = indicators.filter(i => !found.includes(i));
        
        return {
            success: found.length === indicators.length,
            found,
            missing,
            responseLength: response.length
        };
    }

    async testMemoryConsolidationTrigger(): Promise<ConsolidationTestResult> {
        console.log('\n=== Memory Test: Consolidation Trigger ===');
        
        // Simulate a complex task that should trigger consolidation
        const response = await this.harness.sendMessage('I need to implement a complex feature with multiple steps. Can you help me plan it out?');
        
        // Look for consolidation/planning patterns
        const consolidationIndicators = [
            'todo',
            'plan',
            'steps',
            'track',
            'organize'
        ] as const;
        
        console.log('🔍 Checking for consolidation triggers:');
        const found: string[] = [];
        for (const indicator of consolidationIndicators) {
            if (response.toLowerCase().includes(indicator.toLowerCase())) {
                console.log(`🎯 FOUND: ${indicator}`);
                found.push(indicator);
            }
        }
        
        return {
            success: found.length > 0,
            found,
            responseLength: response.length
        };
    }
}

async function main(): Promise<void> {
    const harness = new ClaudeTestHarness();
    const tests = new MemoryBankTests(harness);
    
    try {
        await harness.start();
        
        // Run memory bank tests
        const bootResult = await tests.testBootProcedure();
        const consolidationResult = await tests.testMemoryConsolidationTrigger();
        
        // Summary
        console.log('\n=== Test Summary ===');
        console.log(`Boot Procedure: ${bootResult.success ? '✅ PASS' : '❌ FAIL'}`);
        console.log(`Consolidation Trigger: ${consolidationResult.success ? '✅ PASS' : '❌ FAIL'}`);
        
        if (!bootResult.success) {
            console.log(`Boot missing: ${bootResult.missing.join(', ')}`);
        }
        
        console.log('🎉 Memory test harness working successfully!');
        
    } catch (error) {
        console.error('❌ Error:', error);
    } finally {
        harness.close();
    }
}

if (import.meta.url === `file://${process.argv[1]}`) {
    main();
}